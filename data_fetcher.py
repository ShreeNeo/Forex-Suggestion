"""
Data Fetcher Module for Forex Trading Assistant
Handles fetching real-time and historical XAU/USD data from various free APIs
"""

import requests
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
import logging
import os
import time
from typing import Dict, Optional

logger = logging.getLogger(__name__)


class DataFetcher:
    """Fetch forex data from various free API providers"""

    def __init__(self, config: Dict):
        self.config = config
        self.api_config = config.get('api', {})
        self.provider = self.api_config.get('provider', 'yfinance')
        self.symbol = self.api_config.get('symbol', 'GC=F')  # Gold futures
        self.historical_data_file = config.get('data_storage', {}).get('historical_data_file', 'data/historical_data.csv')

        # Create data directory
        os.makedirs(os.path.dirname(self.historical_data_file), exist_ok=True)

        # Cache for rate limiting
        self.last_fetch_time = 0
        self.min_fetch_interval = 60  # Minimum seconds between API calls

    def fetch_current_price(self) -> Optional[Dict]:
        """
        Fetch current XAU/USD price
        Returns dict with current price, bid, ask, timestamp
        """
        try:
            if self.provider == 'yfinance':
                return self._fetch_yfinance_current()
            elif self.provider == 'alpha_vantage':
                return self._fetch_alpha_vantage_current()
            elif self.provider == 'twelve_data':
                return self._fetch_twelve_data_current()
            else:
                logger.warning(f"Unknown provider: {self.provider}, defaulting to yfinance")
                return self._fetch_yfinance_current()

        except Exception as e:
            logger.error(f"Error fetching current price: {e}")
            return None

    def fetch_historical_data(self, days: int = 30, interval: str = '1h') -> Optional[pd.DataFrame]:
        """
        Fetch historical price data

        Args:
            days: Number of days of historical data
            interval: Data interval (1m, 5m, 15m, 1h, 1d, etc.)

        Returns:
            DataFrame with OHLCV data
        """
        try:
            if self.provider == 'yfinance':
                return self._fetch_yfinance_historical(days, interval)
            elif self.provider == 'alpha_vantage':
                return self._fetch_alpha_vantage_historical(days)
            elif self.provider == 'twelve_data':
                return self._fetch_twelve_data_historical(days, interval)
            else:
                logger.warning(f"Unknown provider: {self.provider}, defaulting to yfinance")
                return self._fetch_yfinance_historical(days, interval)

        except Exception as e:
            logger.error(f"Error fetching historical data: {e}")
            return None

    def _fetch_yfinance_current(self) -> Dict:
        """Fetch current price using yfinance (completely free, no API key needed)"""
        ticker = yf.Ticker(self.symbol)
        info = ticker.info

        # Get the most recent data
        hist = ticker.history(period='1d', interval='1m')

        if hist.empty:
            raise ValueError("No data received from yfinance")

        latest = hist.iloc[-1]

        return {
            'price': latest['Close'],
            'bid': info.get('bid', latest['Close']),
            'ask': info.get('ask', latest['Close']),
            'high': latest['High'],
            'low': latest['Low'],
            'volume': latest['Volume'],
            'timestamp': datetime.now(),
            'spread': info.get('ask', latest['Close']) - info.get('bid', latest['Close'])
        }

    def _fetch_yfinance_historical(self, days: int, interval: str) -> pd.DataFrame:
        """Fetch historical data using yfinance"""
        # Map interval format for yfinance
        interval_map = {
            '1m': '1m',
            '5m': '5m',
            '15m': '15m',
            '1h': '1h',
            '1d': '1d'
        }

        yf_interval = interval_map.get(interval, '1h')

        # Determine period
        if days <= 7:
            period = f'{days}d'
        elif days <= 30:
            period = '1mo'
        elif days <= 90:
            period = '3mo'
        else:
            period = '1y'

        ticker = yf.Ticker(self.symbol)
        data = ticker.history(period=period, interval=yf_interval)

        if data.empty:
            raise ValueError("No historical data received from yfinance")

        # Ensure we have standard column names
        data.columns = ['Open', 'High', 'Low', 'Close', 'Volume', 'Dividends', 'Stock Splits']
        data = data[['Open', 'High', 'Low', 'Close', 'Volume']]
        data.reset_index(inplace=True)
        data.rename(columns={'Date': 'Timestamp'}, inplace=True)

        logger.info(f"Fetched {len(data)} rows of historical data from yfinance")
        return data

    def _fetch_alpha_vantage_current(self) -> Dict:
        """Fetch current price using Alpha Vantage API"""
        api_key = self.api_config.get('alpha_vantage_key')
        if not api_key:
            raise ValueError("Alpha Vantage API key not configured")

        url = f"https://www.alphavantage.co/query"
        params = {
            'function': 'CURRENCY_EXCHANGE_RATE',
            'from_currency': 'XAU',
            'to_currency': 'USD',
            'apikey': api_key
        }

        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        if 'Realtime Currency Exchange Rate' not in data:
            raise ValueError(f"Invalid response from Alpha Vantage: {data}")

        rate_data = data['Realtime Currency Exchange Rate']

        price = float(rate_data['5. Exchange Rate'])
        bid = float(rate_data.get('8. Bid Price', price))
        ask = float(rate_data.get('9. Ask Price', price))

        return {
            'price': price,
            'bid': bid,
            'ask': ask,
            'high': price,  # Alpha Vantage doesn't provide intraday high/low in this endpoint
            'low': price,
            'volume': 0,
            'timestamp': datetime.strptime(rate_data['6. Last Refreshed'], '%Y-%m-%d %H:%M:%S'),
            'spread': ask - bid
        }

    def _fetch_alpha_vantage_historical(self, days: int) -> pd.DataFrame:
        """Fetch historical data using Alpha Vantage API"""
        api_key = self.api_config.get('alpha_vantage_key')
        if not api_key:
            raise ValueError("Alpha Vantage API key not configured")

        # Note: Alpha Vantage free tier is limited, use intraday for recent data
        url = f"https://www.alphavantage.co/query"
        params = {
            'function': 'FX_INTRADAY',
            'from_symbol': 'XAU',
            'to_symbol': 'USD',
            'interval': '60min',
            'outputsize': 'full',
            'apikey': api_key
        }

        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        if 'Time Series FX (60min)' not in data:
            raise ValueError(f"Invalid response from Alpha Vantage: {data}")

        time_series = data['Time Series FX (60min)']

        # Convert to DataFrame
        df = pd.DataFrame.from_dict(time_series, orient='index')
        df.index = pd.to_datetime(df.index)
        df = df.sort_index()

        # Rename columns
        df.columns = ['Open', 'High', 'Low', 'Close']
        df = df.astype(float)
        df['Volume'] = 0  # FX data doesn't have volume

        df.reset_index(inplace=True)
        df.rename(columns={'index': 'Timestamp'}, inplace=True)

        # Filter to requested days
        cutoff = datetime.now() - timedelta(days=days)
        df = df[df['Timestamp'] >= cutoff]

        logger.info(f"Fetched {len(df)} rows of historical data from Alpha Vantage")
        return df

    def _fetch_twelve_data_current(self) -> Dict:
        """Fetch current price using Twelve Data API"""
        api_key = self.api_config.get('twelve_data_key')
        if not api_key:
            raise ValueError("Twelve Data API key not configured")

        url = f"https://api.twelvedata.com/price"
        params = {
            'symbol': 'XAU/USD',
            'apikey': api_key
        }

        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        if 'price' not in data:
            raise ValueError(f"Invalid response from Twelve Data: {data}")

        price = float(data['price'])

        return {
            'price': price,
            'bid': price,  # Twelve Data doesn't provide bid/ask in basic endpoint
            'ask': price,
            'high': price,
            'low': price,
            'volume': 0,
            'timestamp': datetime.now(),
            'spread': 0
        }

    def _fetch_twelve_data_historical(self, days: int, interval: str) -> pd.DataFrame:
        """Fetch historical data using Twelve Data API"""
        api_key = self.api_config.get('twelve_data_key')
        if not api_key:
            raise ValueError("Twelve Data API key not configured")

        url = f"https://api.twelvedata.com/time_series"
        params = {
            'symbol': 'XAU/USD',
            'interval': interval,
            'outputsize': min(days * 24, 5000),  # Max 5000 data points
            'apikey': api_key
        }

        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        if 'values' not in data:
            raise ValueError(f"Invalid response from Twelve Data: {data}")

        df = pd.DataFrame(data['values'])
        df['datetime'] = pd.to_datetime(df['datetime'])
        df = df.sort_values('datetime')

        # Rename and convert columns
        df.rename(columns={
            'datetime': 'Timestamp',
            'open': 'Open',
            'high': 'High',
            'low': 'Low',
            'close': 'Close',
            'volume': 'Volume'
        }, inplace=True)

        df[['Open', 'High', 'Low', 'Close']] = df[['Open', 'High', 'Low', 'Close']].astype(float)
        df['Volume'] = df['Volume'].fillna(0).astype(float)

        logger.info(f"Fetched {len(df)} rows of historical data from Twelve Data")
        return df

    def save_historical_data(self, data: pd.DataFrame):
        """Save historical data to CSV file"""
        try:
            data.to_csv(self.historical_data_file, index=False)
            logger.info(f"Historical data saved to {self.historical_data_file}")
        except Exception as e:
            logger.error(f"Failed to save historical data: {e}")

    def load_historical_data(self) -> Optional[pd.DataFrame]:
        """Load historical data from CSV file"""
        if not os.path.exists(self.historical_data_file):
            logger.warning(f"Historical data file not found: {self.historical_data_file}")
            return None

        try:
            data = pd.read_csv(self.historical_data_file)
            data['Timestamp'] = pd.to_datetime(data['Timestamp'])
            logger.info(f"Loaded {len(data)} rows of historical data from file")
            return data
        except Exception as e:
            logger.error(f"Failed to load historical data: {e}")
            return None

    def update_historical_data(self, days: int = 30, interval: str = '1h') -> pd.DataFrame:
        """
        Update historical data - fetch new data and merge with existing

        Args:
            days: Number of days to fetch
            interval: Data interval

        Returns:
            Updated DataFrame
        """
        # Fetch new data
        new_data = self.fetch_historical_data(days, interval)

        if new_data is None:
            logger.warning("Failed to fetch new data, loading from file")
            return self.load_historical_data()

        # Load existing data
        existing_data = self.load_historical_data()

        if existing_data is not None:
            # Merge and remove duplicates
            combined = pd.concat([existing_data, new_data])
            combined.drop_duplicates(subset=['Timestamp'], keep='last', inplace=True)
            combined.sort_values('Timestamp', inplace=True)
        else:
            combined = new_data

        # Save updated data
        self.save_historical_data(combined)

        return combined

    def get_price_change_24h(self, current_price: float) -> float:
        """Calculate 24-hour price change percentage"""
        try:
            data = self.fetch_historical_data(days=2, interval='1d')
            if data is not None and len(data) >= 2:
                yesterday_close = data.iloc[-2]['Close']
                change = ((current_price - yesterday_close) / yesterday_close) * 100
                return change
        except Exception as e:
            logger.error(f"Failed to calculate 24h change: {e}")

        return 0.0
