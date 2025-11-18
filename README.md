# XAU/USD (Gold) Forex Trading Assistant

A real-time forex trading assistant for XAU/USD (Gold) with automated signal generation, position sizing, and risk management.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## ⚠️ DISCLAIMER

**This tool is for educational purposes only.** Trading forex and commodities involves substantial risk of loss and is not suitable for all investors. Always use paper trading mode to test strategies before risking real capital. The authors are not responsible for any financial losses incurred through the use of this software.

## 🌟 Features

- **Real-time Price Monitoring**: Fetch live XAU/USD data every 1-5 minutes
- **Technical Analysis**:
  - Moving Averages (SMA 20, 50, 200)
  - RSI (Relative Strength Index)
  - MACD (Moving Average Convergence Divergence)
  - Bollinger Bands
  - ATR (Average True Range)
  - Support/Resistance levels
- **Smart Signal Generation**: BUY/SELL signals based on multiple indicator confluence
- **Position Sizing Calculator**: Automatic position sizing based on account balance and risk tolerance
- **Risk Management**:
  - Configurable risk per trade (1-2% recommended)
  - Daily loss limits
  - Maximum positions per day
  - Stop-loss and take-profit calculation
- **Alert System**:
  - Desktop notifications for trading signals
  - Detailed trade recommendations
  - Alert logging with timestamp
- **Paper Trading Mode**: Test strategies without risking real money
- **Clean CLI Interface**: Easy-to-use command-line interface with colored output

## 📋 Requirements

- Python 3.8 or higher
- Internet connection for API access
- (Optional) API keys for Alpha Vantage or Twelve Data

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone <repository-url>
cd Forex-Suggestion
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure the Application

The default configuration uses **yfinance** which requires **NO API KEY** and is completely free!

Edit `config.json` to customize settings:

```json
{
  "api": {
    "provider": "yfinance",
    "symbol": "GC=F"
  },
  "trading": {
    "investment_amount": 10000,
    "risk_percentage_per_trade": 1.5,
    "paper_trading_mode": true
  }
}
```

### 4. Run the Application

```bash
python forex_trader.py
```

## 🔧 Installation Guide

### Step-by-Step Setup

1. **Install Python**: Download from [python.org](https://www.python.org/downloads/)

2. **Create Virtual Environment** (recommended):
   ```bash
   python -m venv venv

   # On Windows:
   venv\Scripts\activate

   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Verify Installation**:
   ```bash
   python -c "import yfinance, pandas, ta; print('All dependencies installed!')"
   ```

## 🔑 API Configuration

The application supports multiple free API providers:

### Option 1: yfinance (Recommended - No API Key Required)

**Advantages**:
- Completely free
- No API key required
- No rate limits for basic usage
- Easy setup

**Setup**: No setup required! This is the default provider.

### Option 2: Alpha Vantage (Free Tier)

**Advantages**:
- 25 API calls per day (free tier)
- Real-time forex data
- Good for intraday trading

**Setup**:
1. Get free API key: [alphavantage.co/support/#api-key](https://www.alphavantage.co/support/#api-key)
2. Update `config.json`:
   ```json
   {
     "api": {
       "provider": "alpha_vantage",
       "alpha_vantage_key": "YOUR_API_KEY_HERE"
     }
   }
   ```

### Option 3: Twelve Data (Free Tier)

**Advantages**:
- 800 API calls per day (free tier)
- Multiple timeframes
- Good data quality

**Setup**:
1. Register at [twelvedata.com](https://twelvedata.com/)
2. Get your API key from the dashboard
3. Update `config.json`:
   ```json
   {
     "api": {
       "provider": "twelve_data",
       "twelve_data_key": "YOUR_API_KEY_HERE"
     }
   }
   ```

## 📊 Usage Guide

### Main Menu Options

1. **🚀 Start Monitoring**: Begin continuous monitoring for trading signals
2. **🔍 Manual Signal Check**: Perform a one-time analysis
3. **⚙️ View/Change Settings**: Customize your preferences
4. **📊 View Alert History**: See your recent trading signals
5. **📈 View Current Trend**: Detailed trend analysis
6. **🧹 Clear Old Alerts**: Remove old alert logs

### Understanding Trading Signals

When a signal is detected, you'll see:

```
📈 TRADING SIGNAL DETECTED 📈
Time: 2024-01-15 14:30:00

ACTION: BUY
Confidence: 83.3% (5/6 indicators)

PRICE INFORMATION:
├─ Current Price: $2045.50
├─ Entry Price: $2045.50
├─ Stop Loss: $2038.75 (67.5 pips)
├─ Take Profit 1: $2055.63 (101.3 pips)
└─ Take Profit 2: $2065.75 (202.5 pips)

POSITION SIZING:
├─ Lot Size: 0.15 lots
├─ Ounces: 15.000 oz
├─ Risk Amount: $150.00
├─ Risk/Reward Ratio: 1:3.00
└─ Potential Profit (TP1): $225.00

TECHNICAL INDICATORS:
├─ RSI: 28.50
├─ MACD: 0.0145
└─ ATR: 3.38

REASONS FOR SIGNAL:
1. RSI oversold (28.50)
2. Bullish MACD crossover
3. Price below lower Bollinger Band
4. Strong bullish momentum (0.85%)
5. Price above SMA 200 (Uptrend)
```

### Configuring Settings

You can customize various settings through the interactive menu:

- **Investment Amount**: Your total trading capital
- **Risk Percentage**: How much to risk per trade (1-2% recommended)
- **Check Interval**: How often to check for signals (in minutes)
- **Paper Trading Mode**: Enable/disable paper trading
- **Notifications**: Enable/disable desktop notifications
- **Daily Loss Limit**: Maximum loss allowed per day
- **Max Positions**: Maximum number of trades per day

## 📁 Project Structure

```
Forex-Suggestion/
├── forex_trader.py          # Main application
├── data_fetcher.py          # API data fetching
├── indicators.py            # Technical analysis
├── position_calculator.py   # Position sizing & risk management
├── alerts.py                # Alert system & notifications
├── config.json              # Configuration file
├── requirements.txt         # Python dependencies
├── README.md                # This file
├── data/                    # Data storage (auto-created)
│   ├── historical_data.csv
│   ├── alert_log.csv
│   └── trade_log.csv
└── forex_trader.log         # Application logs
```

## 🎯 Risk Management Best Practices

1. **Never Risk More Than 1-2% Per Trade**: This ensures you can survive losing streaks
2. **Use Stop Losses**: Always have a predefined exit point
3. **Risk/Reward Ratio**: Aim for at least 1:2 (risk $100 to make $200)
4. **Daily Loss Limit**: Stop trading if you hit your daily limit
5. **Position Sizing**: Let the calculator determine your position size
6. **Paper Trade First**: Test your strategy before using real money

## 🔍 Technical Indicators Explained

### Moving Averages (SMA)
- **SMA 20**: Short-term trend
- **SMA 50**: Medium-term trend
- **SMA 200**: Long-term trend
- **Signal**: Crossovers indicate trend changes

### RSI (Relative Strength Index)
- Range: 0-100
- **< 30**: Oversold (potential buy)
- **> 70**: Overbought (potential sell)

### MACD
- **Bullish Crossover**: MACD crosses above signal line
- **Bearish Crossover**: MACD crosses below signal line

### Bollinger Bands
- **Price < Lower Band**: Potential buy signal
- **Price > Upper Band**: Potential sell signal

### ATR (Average True Range)
- Measures volatility
- Used for stop-loss placement

## 📈 Example Workflow

1. **Start the Application**:
   ```bash
   python forex_trader.py
   ```

2. **Configure Your Settings**:
   - Set investment amount: $10,000
   - Set risk per trade: 1.5%
   - Enable paper trading mode

3. **Start Monitoring**:
   - Select "Start Monitoring" from menu
   - Application checks for signals every 5 minutes

4. **Receive Alert**:
   - Desktop notification appears
   - Detailed signal displayed in console
   - Alert logged to CSV file

5. **Execute Trade** (if in live mode):
   - Review the recommendation
   - Place trade with your broker
   - Set stop-loss and take-profit levels

6. **Monitor Position**:
   - Watch for TP1 or TP2 hit
   - Respect your stop-loss

## 🛠️ Troubleshooting

### Common Issues

**1. "No module named 'xyz'"**
```bash
pip install -r requirements.txt --upgrade
```

**2. "Failed to fetch data"**
- Check your internet connection
- Verify API key (if using Alpha Vantage or Twelve Data)
- Check if you've exceeded API rate limits

**3. "Insufficient data for analysis"**
- Wait for more historical data to be fetched
- Try increasing the `data_history_days` in config.json

**4. Notifications not working**
- Install notification dependencies:
  ```bash
  pip install plyer
  ```
- On Linux, you may need: `apt-get install python3-notify2`

### Debug Mode

Enable detailed logging:
```python
# In forex_trader.py, change logging level to DEBUG
logging.basicConfig(level=logging.DEBUG)
```

## 🔄 Updating Historical Data

The application automatically updates historical data, but you can force an update:

```python
# In Python console
from data_fetcher import DataFetcher
import json

with open('config.json') as f:
    config = json.load(f)

fetcher = DataFetcher(config)
data = fetcher.update_historical_data(days=30, interval='1h')
```

## 📝 Logging

All activities are logged to:
- **forex_trader.log**: Application logs
- **data/alert_log.csv**: Trading alerts
- **data/trade_log.csv**: Trade history (future feature)

## 🚧 Future Enhancements

- [ ] Backtesting functionality
- [ ] Multi-timeframe analysis
- [ ] Telegram bot integration
- [ ] Web dashboard (Flask/Streamlit)
- [ ] Trade journal and performance tracking
- [ ] Additional currency pairs
- [ ] Machine learning signal prediction
- [ ] Integration with broker APIs for automated trading

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details

## 🙏 Acknowledgments

- Market data provided by Yahoo Finance, Alpha Vantage, and Twelve Data
- Technical analysis libraries: pandas-ta, ta
- Community feedback and contributions

## 📞 Support

For issues and questions:
1. Check this README
2. Review the troubleshooting section
3. Check application logs
4. Open an issue on GitHub

## 💡 Tips for Success

1. **Start with Paper Trading**: Test the system thoroughly before risking real money
2. **Keep a Trading Journal**: Log your decisions and learn from them
3. **Don't Override the System**: If daily limits are hit, respect them
4. **Stay Informed**: Follow gold market news and events
5. **Continuous Learning**: Study technical analysis and risk management
6. **Be Patient**: Wait for high-confidence signals (70%+)
7. **Review Alerts**: Check alert history to see what worked

## 📚 Additional Resources

### Learning
- [Investopedia - Technical Analysis](https://www.investopedia.com/technical-analysis-4689657)
- [BabyPips - Forex Education](https://www.babypips.com/learn/forex)
- [TradingView - Charts & Ideas](https://www.tradingview.com/)

### Gold Trading
- [Kitco - Gold News](https://www.kitco.com/gold/)
- [GoldPrice.org](https://goldprice.org/)

### Risk Management
- [Risk Management Guide](https://www.investopedia.com/articles/trading/09/risk-management.asp)

---

**Remember**: Past performance does not guarantee future results. Trade responsibly and never invest more than you can afford to lose.

**Happy Trading! 🚀📈**
