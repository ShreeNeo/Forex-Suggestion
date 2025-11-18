"""
Technical Indicators Module for Forex Trading Assistant
Implements various technical analysis indicators for XAU/USD trading signals
"""

import pandas as pd
import numpy as np
from typing import Dict, Tuple, List
import logging

logger = logging.getLogger(__name__)


class TechnicalIndicators:
    """Calculate and analyze technical indicators for forex trading"""

    def __init__(self, config: Dict):
        self.config = config
        self.indicator_config = config.get('indicators', {})

    def calculate_sma(self, data: pd.DataFrame, period: int, column: str = 'Close') -> pd.Series:
        """Calculate Simple Moving Average"""
        return data[column].rolling(window=period).mean()

    def calculate_ema(self, data: pd.DataFrame, period: int, column: str = 'Close') -> pd.Series:
        """Calculate Exponential Moving Average"""
        return data[column].ewm(span=period, adjust=False).mean()

    def calculate_rsi(self, data: pd.DataFrame, period: int = 14, column: str = 'Close') -> pd.Series:
        """Calculate Relative Strength Index"""
        delta = data[column].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()

        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi

    def calculate_macd(self, data: pd.DataFrame, fast: int = 12, slow: int = 26,
                      signal: int = 9, column: str = 'Close') -> Tuple[pd.Series, pd.Series, pd.Series]:
        """Calculate MACD (Moving Average Convergence Divergence)"""
        exp1 = data[column].ewm(span=fast, adjust=False).mean()
        exp2 = data[column].ewm(span=slow, adjust=False).mean()

        macd = exp1 - exp2
        signal_line = macd.ewm(span=signal, adjust=False).mean()
        histogram = macd - signal_line

        return macd, signal_line, histogram

    def calculate_bollinger_bands(self, data: pd.DataFrame, period: int = 20,
                                 std_dev: int = 2, column: str = 'Close') -> Tuple[pd.Series, pd.Series, pd.Series]:
        """Calculate Bollinger Bands"""
        sma = data[column].rolling(window=period).mean()
        std = data[column].rolling(window=period).std()

        upper_band = sma + (std * std_dev)
        lower_band = sma - (std * std_dev)

        return upper_band, sma, lower_band

    def calculate_atr(self, data: pd.DataFrame, period: int = 14) -> pd.Series:
        """Calculate Average True Range"""
        high = data['High']
        low = data['Low']
        close = data['Close']

        tr1 = high - low
        tr2 = abs(high - close.shift())
        tr3 = abs(low - close.shift())

        tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
        atr = tr.rolling(window=period).mean()

        return atr

    def find_support_resistance(self, data: pd.DataFrame, window: int = 20) -> Dict[str, List[float]]:
        """Find support and resistance levels using local minima and maxima"""
        support_levels = []
        resistance_levels = []

        # Find local minima (support)
        for i in range(window, len(data) - window):
            if data['Low'].iloc[i] == data['Low'].iloc[i-window:i+window].min():
                support_levels.append(data['Low'].iloc[i])

        # Find local maxima (resistance)
        for i in range(window, len(data) - window):
            if data['High'].iloc[i] == data['High'].iloc[i-window:i+window].max():
                resistance_levels.append(data['High'].iloc[i])

        # Keep only recent and unique levels
        support_levels = sorted(set([round(s, 2) for s in support_levels[-5:]]))
        resistance_levels = sorted(set([round(r, 2) for r in resistance_levels[-5:]]))

        return {
            'support': support_levels,
            'resistance': resistance_levels
        }

    def calculate_all_indicators(self, data: pd.DataFrame) -> pd.DataFrame:
        """Calculate all technical indicators and add them to the dataframe"""
        try:
            # Moving Averages
            data['SMA_20'] = self.calculate_sma(data, self.indicator_config.get('sma_short', 20))
            data['SMA_50'] = self.calculate_sma(data, self.indicator_config.get('sma_medium', 50))
            data['SMA_200'] = self.calculate_sma(data, self.indicator_config.get('sma_long', 200))

            # RSI
            data['RSI'] = self.calculate_rsi(data, self.indicator_config.get('rsi_period', 14))

            # MACD
            macd, signal, histogram = self.calculate_macd(
                data,
                self.indicator_config.get('macd_fast', 12),
                self.indicator_config.get('macd_slow', 26),
                self.indicator_config.get('macd_signal', 9)
            )
            data['MACD'] = macd
            data['MACD_Signal'] = signal
            data['MACD_Histogram'] = histogram

            # Bollinger Bands
            upper, middle, lower = self.calculate_bollinger_bands(
                data,
                self.indicator_config.get('bollinger_period', 20),
                self.indicator_config.get('bollinger_std', 2)
            )
            data['BB_Upper'] = upper
            data['BB_Middle'] = middle
            data['BB_Lower'] = lower

            # ATR
            data['ATR'] = self.calculate_atr(data, self.indicator_config.get('atr_period', 14))

            logger.info("All technical indicators calculated successfully")
            return data

        except Exception as e:
            logger.error(f"Error calculating indicators: {e}")
            raise

    def generate_signal(self, data: pd.DataFrame) -> Dict:
        """
        Generate trading signal based on multiple indicator confluence
        Returns: Dict with signal type, strength, and reasons
        """
        if len(data) < 200:
            return {
                'signal': 'HOLD',
                'strength': 0,
                'reasons': ['Insufficient data for analysis'],
                'confidence': 0
            }

        latest = data.iloc[-1]
        prev = data.iloc[-2]

        signals = []
        reasons = []

        # 1. Moving Average Crossover
        if latest['SMA_20'] > latest['SMA_50'] and prev['SMA_20'] <= prev['SMA_50']:
            signals.append('BUY')
            reasons.append('Bullish MA crossover (SMA 20 > SMA 50)')
        elif latest['SMA_20'] < latest['SMA_50'] and prev['SMA_20'] >= prev['SMA_50']:
            signals.append('SELL')
            reasons.append('Bearish MA crossover (SMA 20 < SMA 50)')

        # 2. Long-term trend (SMA 200)
        if latest['Close'] > latest['SMA_200']:
            if 'BUY' in signals:
                reasons.append('Price above SMA 200 (Uptrend)')
        else:
            if 'SELL' in signals:
                reasons.append('Price below SMA 200 (Downtrend)')

        # 3. RSI
        rsi = latest['RSI']
        if rsi < self.indicator_config.get('rsi_oversold', 30):
            signals.append('BUY')
            reasons.append(f'RSI oversold ({rsi:.2f})')
        elif rsi > self.indicator_config.get('rsi_overbought', 70):
            signals.append('SELL')
            reasons.append(f'RSI overbought ({rsi:.2f})')

        # 4. MACD
        if latest['MACD'] > latest['MACD_Signal'] and prev['MACD'] <= prev['MACD_Signal']:
            signals.append('BUY')
            reasons.append('Bullish MACD crossover')
        elif latest['MACD'] < latest['MACD_Signal'] and prev['MACD'] >= prev['MACD_Signal']:
            signals.append('SELL')
            reasons.append('Bearish MACD crossover')

        # 5. Bollinger Bands
        if latest['Close'] < latest['BB_Lower']:
            signals.append('BUY')
            reasons.append('Price below lower Bollinger Band')
        elif latest['Close'] > latest['BB_Upper']:
            signals.append('SELL')
            reasons.append('Price above upper Bollinger Band')

        # 6. Price momentum
        price_change_5 = ((latest['Close'] - data.iloc[-5]['Close']) / data.iloc[-5]['Close']) * 100
        if price_change_5 > 0.5:
            signals.append('BUY')
            reasons.append(f'Strong bullish momentum ({price_change_5:.2f}%)')
        elif price_change_5 < -0.5:
            signals.append('SELL')
            reasons.append(f'Strong bearish momentum ({price_change_5:.2f}%)')

        # Determine final signal based on confluence
        buy_signals = signals.count('BUY')
        sell_signals = signals.count('SELL')

        min_confluence = self.config.get('signal_requirements', {}).get('min_indicators_confluence', 3)

        if buy_signals >= min_confluence and buy_signals > sell_signals:
            signal_type = 'BUY'
            strength = buy_signals
        elif sell_signals >= min_confluence and sell_signals > buy_signals:
            signal_type = 'SELL'
            strength = sell_signals
        else:
            signal_type = 'HOLD'
            strength = 0
            reasons = ['Insufficient indicator confluence']

        # Calculate confidence (0-100)
        confidence = min(100, (strength / 6) * 100)

        return {
            'signal': signal_type,
            'strength': strength,
            'reasons': reasons,
            'confidence': round(confidence, 2),
            'current_price': latest['Close'],
            'rsi': latest['RSI'],
            'macd': latest['MACD'],
            'atr': latest['ATR']
        }

    def get_current_trend(self, data: pd.DataFrame) -> str:
        """Determine the current market trend"""
        if len(data) < 50:
            return "UNKNOWN"

        latest = data.iloc[-1]

        # Check if price is above/below key moving averages
        above_sma20 = latest['Close'] > latest['SMA_20']
        above_sma50 = latest['Close'] > latest['SMA_50']
        above_sma200 = latest['Close'] > latest['SMA_200']

        sma_aligned_bullish = latest['SMA_20'] > latest['SMA_50'] > latest['SMA_200']
        sma_aligned_bearish = latest['SMA_20'] < latest['SMA_50'] < latest['SMA_200']

        if above_sma20 and above_sma50 and above_sma200 and sma_aligned_bullish:
            return "STRONG UPTREND"
        elif above_sma20 and above_sma50:
            return "UPTREND"
        elif not above_sma20 and not above_sma50 and not above_sma200 and sma_aligned_bearish:
            return "STRONG DOWNTREND"
        elif not above_sma20 and not above_sma50:
            return "DOWNTREND"
        else:
            return "SIDEWAYS"
