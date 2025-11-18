#!/usr/bin/env python3
"""
XAU/USD Forex Trading Assistant - Web UI
Beautiful web dashboard with real-time charts and signals
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
import os
from datetime import datetime
import time

from data_fetcher import DataFetcher
from indicators import TechnicalIndicators
from position_calculator import PositionCalculator
from alerts import AlertSystem

# Page configuration
st.set_page_config(
    page_title="XAU/USD Trading Assistant",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #e0e0e0;
    }
    .buy-signal {
        background-color: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 2px solid #28a745;
    }
    .sell-signal {
        background-color: #f8d7da;
        color: #721c24;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 2px solid #dc3545;
    }
    .hold-signal {
        background-color: #fff3cd;
        color: #856404;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 2px solid #ffc107;
    }
</style>
""", unsafe_allow_html=True)


class ForexDashboard:
    """Web dashboard for forex trading assistant"""

    def __init__(self):
        self.load_config()
        self.initialize_components()

    def load_config(self):
        """Load configuration"""
        try:
            with open('config.json', 'r') as f:
                self.config = json.load(f)
        except Exception as e:
            st.error(f"Failed to load config: {e}")
            self.config = {}

    def save_config(self):
        """Save configuration"""
        try:
            with open('config.json', 'w') as f:
                json.dump(self.config, f, indent=2)
            st.success("✅ Configuration saved!")
        except Exception as e:
            st.error(f"Failed to save config: {e}")

    def initialize_components(self):
        """Initialize trading components"""
        self.data_fetcher = DataFetcher(self.config)
        self.indicators = TechnicalIndicators(self.config)
        self.position_calculator = PositionCalculator(self.config)
        self.alert_system = AlertSystem(self.config)

    def fetch_data(self):
        """Fetch current and historical data"""
        with st.spinner("Fetching market data..."):
            # Fetch current price
            current_data = self.data_fetcher.fetch_current_price()

            # Fetch historical data
            historical_data = self.data_fetcher.update_historical_data(
                days=self.config.get('monitoring', {}).get('data_history_days', 30),
                interval='1h'
            )

            if historical_data is not None and len(historical_data) >= 200:
                # Calculate indicators
                historical_data = self.indicators.calculate_all_indicators(historical_data)

            return current_data, historical_data

    def create_candlestick_chart(self, data):
        """Create interactive candlestick chart with indicators"""
        fig = make_subplots(
            rows=4, cols=1,
            shared_xaxes=True,
            vertical_spacing=0.05,
            subplot_titles=('Price & Moving Averages', 'Volume', 'RSI', 'MACD'),
            row_heights=[0.5, 0.15, 0.15, 0.2]
        )

        # Get timestamp column (handle both 'Timestamp' and index)
        if 'Timestamp' in data.columns:
            x_axis = data['Timestamp']
        elif 'Date' in data.columns:
            x_axis = data['Date']
        else:
            x_axis = data.index

        # Candlestick
        fig.add_trace(
            go.Candlestick(
                x=x_axis,
                open=data['Open'],
                high=data['High'],
                low=data['Low'],
                close=data['Close'],
                name='Price'
            ),
            row=1, col=1
        )

        # Moving Averages
        if 'SMA_20' in data.columns:
            fig.add_trace(
                go.Scatter(x=x_axis, y=data['SMA_20'],
                          name='SMA 20', line=dict(color='orange', width=1)),
                row=1, col=1
            )
        if 'SMA_50' in data.columns:
            fig.add_trace(
                go.Scatter(x=x_axis, y=data['SMA_50'],
                          name='SMA 50', line=dict(color='blue', width=1)),
                row=1, col=1
            )
        if 'SMA_200' in data.columns:
            fig.add_trace(
                go.Scatter(x=x_axis, y=data['SMA_200'],
                          name='SMA 200', line=dict(color='red', width=1)),
                row=1, col=1
            )

        # Bollinger Bands
        if 'BB_Upper' in data.columns:
            fig.add_trace(
                go.Scatter(x=x_axis, y=data['BB_Upper'],
                          name='BB Upper', line=dict(color='gray', width=1, dash='dash')),
                row=1, col=1
            )
            fig.add_trace(
                go.Scatter(x=x_axis, y=data['BB_Lower'],
                          name='BB Lower', line=dict(color='gray', width=1, dash='dash'),
                          fill='tonexty', fillcolor='rgba(128,128,128,0.1)'),
                row=1, col=1
            )

        # Volume
        colors = ['red' if row['Open'] > row['Close'] else 'green' for _, row in data.iterrows()]
        fig.add_trace(
            go.Bar(x=x_axis, y=data['Volume'], name='Volume', marker_color=colors),
            row=2, col=1
        )

        # RSI
        if 'RSI' in data.columns:
            fig.add_trace(
                go.Scatter(x=x_axis, y=data['RSI'], name='RSI', line=dict(color='purple')),
                row=3, col=1
            )
            # RSI levels
            fig.add_hline(y=70, line_dash="dash", line_color="red", row=3, col=1)
            fig.add_hline(y=30, line_dash="dash", line_color="green", row=3, col=1)

        # MACD
        if 'MACD' in data.columns:
            fig.add_trace(
                go.Scatter(x=x_axis, y=data['MACD'], name='MACD', line=dict(color='blue')),
                row=4, col=1
            )
            fig.add_trace(
                go.Scatter(x=x_axis, y=data['MACD_Signal'], name='Signal', line=dict(color='red')),
                row=4, col=1
            )
            fig.add_trace(
                go.Bar(x=x_axis, y=data['MACD_Histogram'], name='Histogram'),
                row=4, col=1
            )

        # Update layout
        fig.update_layout(
            height=1000,
            showlegend=True,
            xaxis_rangeslider_visible=False,
            hovermode='x unified',
            template='plotly_white'
        )

        fig.update_xaxes(title_text="Date", row=4, col=1)
        fig.update_yaxes(title_text="Price ($)", row=1, col=1)
        fig.update_yaxes(title_text="Volume", row=2, col=1)
        fig.update_yaxes(title_text="RSI", row=3, col=1)
        fig.update_yaxes(title_text="MACD", row=4, col=1)

        return fig

    def display_current_price(self, current_data):
        """Display current price information"""
        if not current_data:
            st.error("Failed to fetch current price")
            return

        price_change_24h = self.data_fetcher.get_price_change_24h(current_data['price'])

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                label="Current Price",
                value=f"${current_data['price']:.2f}",
                delta=f"{price_change_24h:+.2f}%"
            )

        with col2:
            st.metric(
                label="Bid",
                value=f"${current_data['bid']:.2f}"
            )

        with col3:
            st.metric(
                label="Ask",
                value=f"${current_data['ask']:.2f}"
            )

        with col4:
            st.metric(
                label="Spread",
                value=f"${current_data['spread']:.2f}"
            )

    def display_signal(self, signal_data, current_data):
        """Display trading signal"""
        if not signal_data:
            return

        signal_type = signal_data['signal']

        # Choose styling based on signal
        if signal_type == 'BUY':
            css_class = "buy-signal"
            icon = "📈"
        elif signal_type == 'SELL':
            css_class = "sell-signal"
            icon = "📉"
        else:
            css_class = "hold-signal"
            icon = "⏸️"

        st.markdown(f"""
        <div class="{css_class}">
            <h2>{icon} {signal_type} SIGNAL</h2>
            <h3>Confidence: {signal_data['confidence']:.1f}% ({signal_data['strength']}/6 indicators)</h3>
        </div>
        """, unsafe_allow_html=True)

        # Calculate position if signal is actionable
        if signal_type in ['BUY', 'SELL']:
            try:
                position_data = self.position_calculator.calculate_position(
                    signal_type,
                    signal_data['current_price'],
                    signal_data['atr']
                )

                # Display position details
                col1, col2, col3 = st.columns(3)

                with col1:
                    st.markdown("### 💰 Entry & Targets")
                    st.write(f"**Entry Price:** ${position_data['entry_price']:.2f}")
                    st.write(f"**Stop Loss:** ${position_data['stop_loss']:.2f} ({position_data['stop_loss_pips']:.1f} pips)")
                    st.write(f"**Take Profit 1:** ${position_data['take_profit_1']:.2f} ({position_data['tp1_pips']:.1f} pips)")
                    st.write(f"**Take Profit 2:** ${position_data['take_profit_2']:.2f} ({position_data['tp2_pips']:.1f} pips)")

                with col2:
                    st.markdown("### 📊 Position Sizing")
                    st.write(f"**Lot Size:** {position_data['lot_size']:.2f} lots")
                    st.write(f"**Ounces:** {position_data['ounces']:.3f} oz")
                    st.write(f"**Risk Amount:** ${position_data['risk_amount']:.2f}")
                    st.write(f"**Potential Profit (TP1):** ${position_data['potential_profit_tp1']:.2f}")
                    st.write(f"**Risk/Reward Ratio:** 1:{position_data['risk_reward_ratio']:.2f}")

                with col3:
                    st.markdown("### 📈 Technical Indicators")
                    st.write(f"**RSI:** {signal_data['rsi']:.2f}")
                    st.write(f"**MACD:** {signal_data['macd']:.4f}")
                    st.write(f"**ATR:** {signal_data['atr']:.2f}")

                # Display reasons
                st.markdown("### 🎯 Signal Reasons")
                for i, reason in enumerate(signal_data['reasons'], 1):
                    st.write(f"{i}. {reason}")

            except Exception as e:
                st.error(f"Error calculating position: {e}")

    def display_indicators_table(self, data):
        """Display current indicator values in a table"""
        if data is None or len(data) == 0:
            return

        latest = data.iloc[-1]

        indicators_data = {
            'Indicator': [
                'SMA 20', 'SMA 50', 'SMA 200',
                'RSI', 'MACD', 'MACD Signal',
                'BB Upper', 'BB Middle', 'BB Lower',
                'ATR'
            ],
            'Value': [
                f"${latest.get('SMA_20', 0):.2f}",
                f"${latest.get('SMA_50', 0):.2f}",
                f"${latest.get('SMA_200', 0):.2f}",
                f"{latest.get('RSI', 0):.2f}",
                f"{latest.get('MACD', 0):.4f}",
                f"{latest.get('MACD_Signal', 0):.4f}",
                f"${latest.get('BB_Upper', 0):.2f}",
                f"${latest.get('BB_Middle', 0):.2f}",
                f"${latest.get('BB_Lower', 0):.2f}",
                f"{latest.get('ATR', 0):.2f}"
            ]
        }

        st.table(pd.DataFrame(indicators_data))

    def display_alert_history(self):
        """Display recent alerts"""
        alerts = self.alert_system.get_recent_alerts(limit=20)

        if not alerts:
            st.info("No alerts yet. Start monitoring to generate signals!")
            return

        # Convert to DataFrame
        df = pd.DataFrame(alerts)

        # Format timestamp
        df['Timestamp'] = pd.to_datetime(df['Timestamp']).dt.strftime('%Y-%m-%d %H:%M')

        # Select columns to display
        display_cols = ['Timestamp', 'Signal', 'Entry_Price', 'Stop_Loss',
                       'Take_Profit_1', 'Lot_Size', 'Confidence', 'Risk_Amount']

        if all(col in df.columns for col in display_cols):
            df_display = df[display_cols].copy()

            # Format numeric columns
            for col in ['Entry_Price', 'Stop_Loss', 'Take_Profit_1', 'Risk_Amount']:
                df_display[col] = df_display[col].astype(float).apply(lambda x: f"${x:.2f}")

            df_display['Lot_Size'] = df_display['Lot_Size'].astype(float).apply(lambda x: f"{x:.2f}")
            df_display['Confidence'] = df_display['Confidence'].astype(float).apply(lambda x: f"{x:.0f}%")

            st.dataframe(df_display, use_container_width=True)

    def sidebar_settings(self):
        """Sidebar with settings"""
        st.sidebar.title("⚙️ Settings")

        # Trading settings
        st.sidebar.subheader("💼 Trading Configuration")

        investment = st.sidebar.number_input(
            "Investment Amount ($)",
            min_value=20,
            max_value=1000000,
            value=self.config.get('trading', {}).get('investment_amount', 10000),
            step=10
        )

        risk_pct = st.sidebar.slider(
            "Risk per Trade (%)",
            min_value=0.0,
            max_value=20.0,
            value=self.config.get('trading', {}).get('risk_percentage_per_trade', 1.5),
            step=0.1
        )

        paper_trading = st.sidebar.checkbox(
            "Paper Trading Mode",
            value=self.config.get('trading', {}).get('paper_trading_mode', True)
        )

        max_positions = st.sidebar.number_input(
            "Max Positions per Day",
            min_value=1,
            max_value=10,
            value=self.config.get('trading', {}).get('max_positions_per_day', 3)
        )

        daily_loss_limit = st.sidebar.number_input(
            "Daily Loss Limit ($)",
            min_value=0,
            max_value=100000,
            value=self.config.get('trading', {}).get('daily_loss_limit', 300),
            step=10
        )

        # Monitoring settings
        st.sidebar.subheader("🔍 Monitoring")

        check_interval = st.sidebar.slider(
            "Check Interval (minutes)",
            min_value=1,
            max_value=60,
            value=self.config.get('monitoring', {}).get('check_interval_minutes', 5)
        )

        min_confluence = st.sidebar.slider(
            "Min Indicators Confluence",
            min_value=2,
            max_value=6,
            value=self.config.get('signal_requirements', {}).get('min_indicators_confluence', 3)
        )

        # Save button
        if st.sidebar.button("💾 Save Settings"):
            self.config['trading']['investment_amount'] = investment
            self.config['trading']['risk_percentage_per_trade'] = risk_pct
            self.config['trading']['paper_trading_mode'] = paper_trading
            self.config['trading']['max_positions_per_day'] = max_positions
            self.config['trading']['daily_loss_limit'] = daily_loss_limit
            self.config['monitoring']['check_interval_minutes'] = check_interval
            self.config['signal_requirements']['min_indicators_confluence'] = min_confluence

            self.save_config()
            self.initialize_components()

        # Info
        st.sidebar.markdown("---")
        st.sidebar.info(f"""
        **Account Summary**
        - Investment: ${investment:,.2f}
        - Risk/Trade: {risk_pct}%
        - Mode: {'Paper' if paper_trading else 'Live'}
        - Max Daily Loss: ${daily_loss_limit}
        """)

        st.sidebar.warning("⚠️ **Disclaimer:** Educational purposes only. Trading involves risk.")

    def run(self):
        """Run the dashboard"""
        # Header
        st.markdown('<h1 class="main-header">📈 XAU/USD Forex Trading Assistant</h1>', unsafe_allow_html=True)
        st.markdown("Real-time Gold trading signals with technical analysis and risk management")

        # Sidebar
        self.sidebar_settings()

        # Auto-refresh option
        auto_refresh = st.checkbox("🔄 Auto-refresh (every 5 minutes)", value=False)

        if auto_refresh:
            st.info("Dashboard will auto-refresh in 5 minutes...")

        # Manual refresh button
        if st.button("🔄 Refresh Data Now"):
            st.rerun()

        # Fetch data
        current_data, historical_data = self.fetch_data()

        # Display current price
        st.subheader("💰 Current Market Data")
        self.display_current_price(current_data)

        # Generate signal
        if historical_data is not None and len(historical_data) >= 200:
            signal_data = self.indicators.generate_signal(historical_data)
            trend = self.indicators.get_current_trend(historical_data)

            # Display trend
            st.markdown(f"**Current Trend:** {trend}")

            # Tabs for different views
            tab1, tab2, tab3, tab4 = st.tabs(["📊 Charts", "🎯 Signal", "📋 Indicators", "📜 Alert History"])

            with tab1:
                st.subheader("Price Chart with Technical Indicators")
                chart = self.create_candlestick_chart(historical_data.tail(200))
                st.plotly_chart(chart, use_container_width=True)

            with tab2:
                st.subheader("Trading Signal")
                self.display_signal(signal_data, current_data)

            with tab3:
                st.subheader("Technical Indicators")
                col1, col2 = st.columns([1, 1])
                with col1:
                    self.display_indicators_table(historical_data)
                with col2:
                    # Support/Resistance
                    levels = self.indicators.find_support_resistance(historical_data)
                    st.markdown("### 📍 Support & Resistance Levels")
                    if levels['support']:
                        st.write("**Support:**", ", ".join([f"${s:.2f}" for s in levels['support']]))
                    if levels['resistance']:
                        st.write("**Resistance:**", ", ".join([f"${r:.2f}" for r in levels['resistance']]))

            with tab4:
                st.subheader("Recent Alerts")
                self.display_alert_history()

        else:
            st.warning("Insufficient data for analysis. Please wait while data is being fetched...")

        # Auto-refresh logic
        if auto_refresh:
            time.sleep(300)  # 5 minutes
            st.rerun()


def main():
    """Main entry point"""
    dashboard = ForexDashboard()
    dashboard.run()


if __name__ == '__main__':
    main()
