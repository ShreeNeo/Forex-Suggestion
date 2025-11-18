# 🌐 Web UI Guide - XAU/USD Forex Trading Assistant

## Beautiful Dashboard with Interactive Charts!

This guide will help you set up and use the web-based dashboard for a much better visual experience than the command-line interface.

## 🎨 What You'll Get

The web UI provides:

- **📊 Interactive Price Charts** - Candlestick charts with zoom and hover
- **📈 Technical Indicators Overlay** - Moving averages, Bollinger Bands, RSI, MACD
- **🎯 Real-time Signals** - Visual alerts with entry/exit prices
- **💰 Position Calculator** - Automatic risk management display
- **📋 Alert History Table** - All your past signals in one place
- **⚙️ Settings Panel** - Easy configuration without editing JSON
- **🔄 Auto-refresh** - Dashboard updates automatically
- **📱 Responsive Design** - Works on desktop, tablet, and mobile

## 🚀 Quick Start

### Option 1: Use the Launcher Script

**Linux/macOS:**
```bash
./start_web.sh
```

**Windows:**
```batch
start_web.bat
```

The dashboard will automatically open in your browser at `http://localhost:8501`

### Option 2: Manual Start

```bash
# Make sure virtual environment is activated
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate.bat  # Windows

# Start the web UI
streamlit run web_ui.py
```

## 📸 Dashboard Features

### 1. **Current Market Data** (Top Section)

Four metric cards showing:
- Current Price with 24h change
- Bid price
- Ask price
- Spread

### 2. **Main Tabs**

#### 📊 Charts Tab
- **Candlestick Chart**: Visual price action
- **Moving Averages**: SMA 20, 50, 200 overlaid
- **Bollinger Bands**: Volatility bands
- **Volume Bar Chart**: Trading volume
- **RSI Chart**: Overbought/oversold indicator
- **MACD Chart**: Momentum indicator

All charts are **interactive**:
- 🔍 Zoom in/out
- 👆 Hover for values
- 📅 Time range selection
- 💾 Download as image

#### 🎯 Signal Tab
Shows trading recommendations:
- Signal type (BUY/SELL/HOLD)
- Confidence percentage
- Entry price
- Stop loss level
- Take profit targets (TP1, TP2)
- Position sizing (lots, ounces)
- Risk amount in dollars
- Risk/reward ratio
- Technical indicator values
- Reasons for the signal

#### 📋 Indicators Tab
- Complete table of all technical indicators
- Current values for:
  - All moving averages
  - RSI
  - MACD values
  - Bollinger Band levels
  - ATR
- Support and resistance levels

#### 📜 Alert History Tab
- Table of all past alerts
- Sortable and searchable
- Shows:
  - Timestamp
  - Signal type
  - Entry price
  - Stop loss
  - Take profit
  - Lot size
  - Confidence
  - Risk amount

### 3. **Sidebar Settings** (Left Panel)

#### 💼 Trading Configuration
- **Investment Amount**: Your trading capital
- **Risk per Trade**: Percentage to risk (0.5% - 5%)
- **Paper Trading Mode**: Toggle on/off
- **Max Positions per Day**: Limit daily trades
- **Daily Loss Limit**: Maximum daily loss

#### 🔍 Monitoring
- **Check Interval**: How often to check (1-60 minutes)
- **Min Indicators Confluence**: How many indicators must agree (2-6)

#### 💾 Save Button
Click to save your settings to config.json

#### 📊 Account Summary
Real-time display of your current settings

### 4. **Control Buttons** (Top)

- **🔄 Auto-refresh**: Automatically update every 5 minutes
- **🔄 Refresh Data Now**: Manual refresh

## 🎯 How to Use the Dashboard

### First Time Setup

1. **Start the dashboard**:
   ```bash
   ./start_web.sh
   ```

2. **Browser opens automatically** at `http://localhost:8501`

3. **Configure your settings** in the sidebar:
   - Set your investment amount
   - Adjust risk percentage
   - **Keep paper trading ON** for testing
   - Click "Save Settings"

4. **Click "Refresh Data Now"** to fetch live data

5. **Explore the tabs**:
   - Check the charts
   - Look at current signals
   - Review indicators

### Daily Trading Workflow

1. **Open the dashboard**:
   ```bash
   ./start_web.sh
   ```

2. **Enable Auto-refresh**:
   - Check the "Auto-refresh" box
   - Dashboard updates every 5 minutes

3. **Monitor the Signal tab**:
   - Wait for BUY or SELL signals
   - Check confidence level (>70% recommended)
   - Review the reasons

4. **When you get a signal**:
   - Note the entry price
   - Set your stop loss
   - Set your take profit targets
   - Check position sizing
   - Decide whether to take the trade

5. **Track in Alert History**:
   - All signals are logged
   - Review past performance
   - Learn from the signals

## 📊 Understanding the Charts

### Price Chart (Top)
- **Green candles**: Price went up
- **Red candles**: Price went down
- **Orange line**: Short-term trend (SMA 20)
- **Blue line**: Medium-term trend (SMA 50)
- **Red line**: Long-term trend (SMA 200)
- **Gray bands**: Bollinger Bands (volatility)

### Volume Chart
- **Green bars**: Buying volume
- **Red bars**: Selling volume

### RSI Chart
- **Above 70**: Overbought (potential sell)
- **Below 30**: Oversold (potential buy)
- **Middle 50**: Neutral

### MACD Chart
- **Blue line**: MACD
- **Red line**: Signal line
- **Bars**: Histogram (momentum)
- **Crossover**: Potential signal

## ⚙️ Customization Tips

### Conservative Settings
```
Investment: $10,000
Risk per Trade: 1.0%
Max Positions: 2
Min Indicators: 4
Check Interval: 15 minutes
```

### Moderate Settings (Recommended)
```
Investment: $10,000
Risk per Trade: 1.5%
Max Positions: 3
Min Indicators: 3
Check Interval: 5 minutes
```

### Aggressive Settings
```
Investment: $10,000
Risk per Trade: 2.0%
Max Positions: 5
Min Indicators: 2
Check Interval: 5 minutes
```

## 🔄 Auto-Refresh Feature

When enabled:
- Dashboard refreshes every 5 minutes
- Automatically fetches new data
- Updates all charts and indicators
- Generates new signals if conditions met

**Perfect for**:
- Continuous monitoring
- Leaving dashboard open all day
- Not missing any signals

## 📱 Mobile Access

The dashboard works on mobile devices!

**To access from your phone** (on same WiFi):

1. Find your computer's IP address:
   ```bash
   # Linux/macOS
   ifconfig | grep "inet "

   # Windows
   ipconfig
   ```

2. Look for something like `192.168.1.100`

3. Start the dashboard with network access:
   ```bash
   streamlit run web_ui.py --server.address 0.0.0.0
   ```

4. On your phone's browser, go to:
   ```
   http://192.168.1.100:8501
   ```

## 🎨 Color Coding

- **🟢 Green**: Bullish signals, profits, increases
- **🔴 Red**: Bearish signals, losses, decreases
- **🟡 Yellow**: Warnings, neutral, HOLD signals
- **🔵 Blue**: Information, indicators

## 💡 Pro Tips

1. **Use multiple timeframes**: Look at 1h, 4h, and daily charts
2. **Wait for high confidence**: Only trade signals >70% confidence
3. **Check confluence**: Ensure multiple indicators agree
4. **Use stop losses**: Always protect your capital
5. **Start with paper trading**: Test for at least a week
6. **Keep dashboard open**: Use auto-refresh during trading hours
7. **Review history**: Learn from past signals in Alert History tab

## 🐛 Troubleshooting

### Dashboard won't start
```bash
# Check if streamlit is installed
pip install streamlit plotly

# Try manual start
streamlit run web_ui.py
```

### Data not loading
- Check internet connection
- Wait 30 seconds and click "Refresh Data Now"
- Check forex_trader.log for errors

### Charts not showing
```bash
# Install plotly
pip install plotly kaleido
```

### Port already in use
```bash
# Use a different port
streamlit run web_ui.py --server.port 8502
```

### Browser doesn't open automatically
Manually go to: `http://localhost:8501`

## 🚀 Performance Tips

1. **Clear old alerts**: Use the CLI option to remove old data
2. **Reduce data history**: Set `data_history_days` to 7 instead of 30
3. **Increase refresh interval**: Set to 15 or 30 minutes if needed
4. **Close unused tabs**: Keep only the tab you're viewing

## 📊 Comparing Web UI vs CLI

| Feature | Web UI | CLI |
|---------|--------|-----|
| Visual Charts | ✅ Yes | ❌ No |
| Interactive | ✅ Yes | ❌ No |
| Easy Settings | ✅ Yes | ⚠️ Manual |
| Mobile Access | ✅ Yes | ❌ No |
| Real-time Updates | ✅ Auto | ⚠️ Manual |
| Resource Usage | ⚠️ Higher | ✅ Lower |
| Setup Complexity | ⚠️ More deps | ✅ Simple |

**Recommendation**: Use Web UI for daily trading, CLI for quick checks or server deployment

## 🔐 Security Notes

- Dashboard runs **locally** on your computer
- Data is **not sent** to external servers
- To allow remote access, use VPN or SSH tunnel
- Don't expose to public internet without authentication

## 🎓 Learning Resources

### Understanding the Dashboard
1. Start with "Charts" tab - learn to read candlesticks
2. Move to "Indicators" tab - understand each indicator
3. Study "Signal" tab - see how indicators combine
4. Review "Alert History" - learn from past signals

### Practice Workflow
1. Week 1: Just observe, don't trade
2. Week 2: Paper trade all signals
3. Week 3: Paper trade only high-confidence (>75%)
4. Week 4: Analyze results, adjust settings
5. Week 5+: Consider live trading (if profitable)

## 📞 Getting Help

1. Check this guide
2. Read main README.md
3. Check browser console for errors (F12)
4. Look at forex_trader.log
5. Verify all dependencies installed

## 🎉 Enjoy Your Dashboard!

You now have a professional-grade trading dashboard with:
- Beautiful charts
- Real-time data
- Automated signals
- Risk management
- Complete history

**Start with paper trading and good luck!** 🚀📈

---

**Quick Commands Reference:**

```bash
# Start web UI
./start_web.sh

# Stop (in terminal where it's running)
Ctrl+C

# Install dependencies
pip install -r requirements.txt

# Update to latest
git pull origin <branch-name>
```
