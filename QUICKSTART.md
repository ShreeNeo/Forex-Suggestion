# Quick Start Guide

Get started with the XAU/USD Forex Trading Assistant in 5 minutes!

## 1. Prerequisites

- Python 3.8 or higher installed
- Internet connection

## 2. Installation

### On Linux/macOS:

```bash
# Run the setup script
./setup.sh

# Or manually:
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### On Windows:

```batch
REM Run the setup script
setup.bat

REM Or manually:
python -m venv venv
venv\Scripts\activate.bat
pip install -r requirements.txt
```

## 3. First Run

```bash
# Make sure virtual environment is activated
python forex_trader.py
```

## 4. What to Expect

### Main Menu:
```
═══ MAIN MENU ═══

1. 🚀 Start Monitoring
2. 🔍 Manual Signal Check
3. ⚙️  View/Change Settings
4. 📊 View Alert History
5. 📈 View Current Trend
6. 🧹 Clear Old Alerts
0. 🚪 Exit
```

### First Steps:

1. **Configure Settings** (Option 3):
   - Set your investment amount (e.g., $10,000)
   - Set risk per trade (recommended: 1-2%)
   - **Keep paper trading mode ON** for testing

2. **Try Manual Check** (Option 2):
   - See how the system analyzes current market
   - View technical indicators
   - Get a feel for the signals

3. **View Current Trend** (Option 5):
   - Understand current market conditions
   - See all technical indicators

4. **Start Monitoring** (Option 1):
   - Begin automatic signal detection
   - Receive alerts when opportunities arise
   - Press Ctrl+C to stop

## 5. Understanding Your First Signal

When a signal appears, you'll see:

```
📈 TRADING SIGNAL DETECTED 📈

ACTION: BUY
Confidence: 83.3% (5/6 indicators)

PRICE INFORMATION:
├─ Entry Price: $2045.50
├─ Stop Loss: $2038.75
├─ Take Profit 1: $2055.63
└─ Take Profit 2: $2065.75

POSITION SIZING:
├─ Lot Size: 0.15 lots
├─ Risk Amount: $150.00
└─ Risk/Reward Ratio: 1:3.00
```

**What does this mean?**
- **Entry Price**: Price to enter the trade
- **Stop Loss**: Exit here if trade goes against you (limit losses)
- **Take Profit**: Exit here to lock in profits
- **Lot Size**: Position size calculated based on your risk settings
- **Risk Amount**: How much you could lose if stop loss is hit

## 6. Important Safety Rules

### ⚠️ ALWAYS:
- Start with **paper trading mode** enabled
- Test the system for at least a week
- Review all alerts and understand why they were triggered
- Respect daily loss limits
- Use stop losses

### ❌ NEVER:
- Disable paper trading without testing first
- Risk more than 2% per trade
- Ignore stop losses
- Chase losses
- Trade with money you can't afford to lose

## 7. Configuration Tips

### Recommended Settings for Beginners:

```json
{
  "trading": {
    "investment_amount": 10000,
    "risk_percentage_per_trade": 1.5,
    "paper_trading_mode": true,
    "max_positions_per_day": 3,
    "daily_loss_limit": 300
  },
  "monitoring": {
    "check_interval_minutes": 5,
    "enable_notifications": true
  }
}
```

### Aggressive Settings (Advanced):

```json
{
  "trading": {
    "risk_percentage_per_trade": 2.0,
    "max_positions_per_day": 5
  },
  "signal_requirements": {
    "min_indicators_confluence": 2
  }
}
```

### Conservative Settings:

```json
{
  "trading": {
    "risk_percentage_per_trade": 1.0,
    "max_positions_per_day": 2
  },
  "signal_requirements": {
    "min_indicators_confluence": 4
  }
}
```

## 8. Common Commands

```bash
# Start the application
python forex_trader.py

# Check logs
tail -f forex_trader.log

# View recent alerts
cat data/alert_log.csv

# Update configuration
nano config.json  # or use any text editor
```

## 9. Troubleshooting

### "No module named 'pandas'"
```bash
pip install -r requirements.txt
```

### Notifications not working
```bash
# On Linux:
sudo apt-get install python3-notify2

# Then reinstall:
pip install plyer
```

### No data available
- Check internet connection
- Wait a few minutes for data to download
- Try manual check first (Option 2)

## 10. Next Steps

1. **Learn the Indicators**: Understand RSI, MACD, Moving Averages
2. **Keep a Journal**: Track why you would/wouldn't take each signal
3. **Review Performance**: Check alert history regularly
4. **Gradual Increase**: Only increase risk after proven success
5. **Stay Informed**: Follow gold market news

## 11. Getting Help

- Read the full [README.md](README.md)
- Check application logs: `forex_trader.log`
- Review alert history: `data/alert_log.csv`
- Test with manual checks before live monitoring

## 12. Your First Week

### Day 1-2: Setup & Learning
- Install and configure
- Run manual checks
- Understand the indicators

### Day 3-4: Paper Trading
- Enable monitoring
- Observe signals
- Take notes on each signal

### Day 5-7: Analysis
- Review alert history
- Calculate theoretical performance
- Adjust settings if needed

## Ready to Start?

```bash
python forex_trader.py
```

**Remember**: This is a tool to assist your trading decisions, not to make them for you. Always do your own analysis and never risk more than you can afford to lose.

Good luck! 🚀
