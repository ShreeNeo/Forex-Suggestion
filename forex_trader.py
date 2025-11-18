#!/usr/bin/env python3
"""
XAU/USD (Gold) Forex Trading Assistant
Real-time trading signals and position sizing for gold forex trading

DISCLAIMER: This tool is for educational purposes only. Trading forex and
commodities involves substantial risk of loss. Always use paper trading mode
to test strategies before risking real capital.
"""

import json
import os
import sys
import time
import logging
from datetime import datetime
from typing import Dict, Optional
import signal as system_signal

from colorama import init, Fore, Style
from tabulate import tabulate

from data_fetcher import DataFetcher
from indicators import TechnicalIndicators
from position_calculator import PositionCalculator
from alerts import AlertSystem

# Initialize colorama for cross-platform colored output
init(autoreset=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('forex_trader.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


class ForexTradingAssistant:
    """Main application class for forex trading assistant"""

    def __init__(self, config_file: str = 'config.json'):
        self.config_file = config_file
        self.config = self.load_config()
        self.running = False
        self.monitoring = False

        # Initialize components
        self.data_fetcher = DataFetcher(self.config)
        self.indicators = TechnicalIndicators(self.config)
        self.position_calculator = PositionCalculator(self.config)
        self.alert_system = AlertSystem(self.config)

        # Trading state
        self.last_signal = None
        self.last_signal_time = None
        self.trades_today = 0
        self.daily_loss = 0.0

        # Setup signal handler for graceful shutdown
        system_signal.signal(system_signal.SIGINT, self.signal_handler)

    def load_config(self) -> Dict:
        """Load configuration from JSON file"""
        try:
            with open(self.config_file, 'r') as f:
                config = json.load(f)
            logger.info(f"Configuration loaded from {self.config_file}")
            return config
        except FileNotFoundError:
            logger.error(f"Configuration file not found: {self.config_file}")
            sys.exit(1)
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in configuration file: {e}")
            sys.exit(1)

    def save_config(self):
        """Save current configuration to file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
            logger.info("Configuration saved")
        except Exception as e:
            logger.error(f"Failed to save configuration: {e}")

    def signal_handler(self, signum, frame):
        """Handle Ctrl+C gracefully"""
        print(f"\n{Fore.YELLOW}Shutting down gracefully...{Style.RESET_ALL}")
        self.stop_monitoring()
        sys.exit(0)

    def display_banner(self):
        """Display application banner"""
        banner = f"""
{Fore.CYAN}╔════════════════════════════════════════════════════════════════╗
║          XAU/USD (Gold) Forex Trading Assistant               ║
║                                                                ║
║  Real-time signals • Position sizing • Risk management        ║
╚════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}

{Fore.YELLOW}⚠️  DISCLAIMER: For educational purposes only. Trading involves risk.{Style.RESET_ALL}
{Fore.YELLOW}    Paper trading mode: {self.config['trading']['paper_trading_mode']}{Style.RESET_ALL}
"""
        print(banner)

    def display_dashboard(self, current_data: Dict, signal_data: Optional[Dict] = None):
        """Display main trading dashboard"""
        os.system('clear' if os.name == 'posix' else 'cls')
        self.display_banner()

        # Current price information
        price_change_24h = self.data_fetcher.get_price_change_24h(current_data['price'])
        change_color = Fore.GREEN if price_change_24h >= 0 else Fore.RED
        change_symbol = "▲" if price_change_24h >= 0 else "▼"

        print(f"\n{Fore.CYAN}═══ CURRENT MARKET DATA ═══{Style.RESET_ALL}")
        print(f"Symbol: XAU/USD (Gold)")
        print(f"Price: {Fore.YELLOW}${current_data['price']:.2f}{Style.RESET_ALL}")
        print(f"24h Change: {change_color}{change_symbol} {price_change_24h:+.2f}%{Style.RESET_ALL}")
        print(f"Bid/Ask: ${current_data['bid']:.2f} / ${current_data['ask']:.2f}")
        print(f"Spread: ${current_data['spread']:.2f}")
        print(f"Last Update: {current_data['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}")

        # Signal information
        if signal_data:
            print(f"\n{Fore.CYAN}═══ TRADING SIGNALS ═══{Style.RESET_ALL}")

            signal_type = signal_data['signal']
            if signal_type == 'BUY':
                signal_color = Fore.GREEN
                signal_icon = "📈"
            elif signal_type == 'SELL':
                signal_color = Fore.RED
                signal_icon = "📉"
            else:
                signal_color = Fore.YELLOW
                signal_icon = "⏸️"

            print(f"Signal: {signal_color}{signal_icon} {signal_type}{Style.RESET_ALL}")
            print(f"Confidence: {signal_data['confidence']:.1f}% ({signal_data['strength']}/6 indicators)")

            print(f"\n{Fore.CYAN}Technical Indicators:{Style.RESET_ALL}")
            print(f"  RSI: {signal_data['rsi']:.2f}")
            print(f"  MACD: {signal_data['macd']:.4f}")
            print(f"  ATR: {signal_data['atr']:.2f}")

            if signal_data['reasons']:
                print(f"\n{Fore.CYAN}Signal Reasons:{Style.RESET_ALL}")
                for i, reason in enumerate(signal_data['reasons'], 1):
                    print(f"  {i}. {reason}")

        # Account information
        print(f"\n{Fore.CYAN}═══ ACCOUNT INFORMATION ═══{Style.RESET_ALL}")
        print(f"Investment Amount: ${self.config['trading']['investment_amount']:,.2f}")
        print(f"Risk per Trade: {self.config['trading']['risk_percentage_per_trade']:.1f}%")
        print(f"Trades Today: {self.trades_today}/{self.config['trading']['max_positions_per_day']}")
        print(f"Daily Loss: ${self.daily_loss:.2f}")

        # Monitoring status
        status_icon = "🟢" if self.monitoring else "🔴"
        status_text = "ACTIVE" if self.monitoring else "STOPPED"
        status_color = Fore.GREEN if self.monitoring else Fore.RED
        print(f"\nMonitoring Status: {status_icon} {status_color}{status_text}{Style.RESET_ALL}")

        if self.last_signal_time:
            print(f"Last Alert: {self.last_signal_time.strftime('%Y-%m-%d %H:%M:%S')}")

    def fetch_and_analyze(self) -> tuple:
        """Fetch current data and perform technical analysis"""
        try:
            # Fetch current price
            current_data = self.data_fetcher.fetch_current_price()
            if not current_data:
                logger.error("Failed to fetch current price")
                return None, None

            # Update and fetch historical data
            historical_data = self.data_fetcher.update_historical_data(
                days=self.config['monitoring']['data_history_days'],
                interval='1h'
            )

            if historical_data is None or len(historical_data) < 200:
                logger.warning("Insufficient historical data for analysis")
                return current_data, None

            # Calculate indicators
            historical_data = self.indicators.calculate_all_indicators(historical_data)

            # Generate signal
            signal_data = self.indicators.generate_signal(historical_data)

            return current_data, signal_data

        except Exception as e:
            logger.error(f"Error in fetch_and_analyze: {e}")
            return None, None

    def check_for_signals(self):
        """Check for trading signals and trigger alerts if conditions are met"""
        current_data, signal_data = self.fetch_and_analyze()

        if not current_data or not signal_data:
            return

        # Display dashboard
        self.display_dashboard(current_data, signal_data)

        # Check if we have a valid trading signal
        if signal_data['signal'] in ['BUY', 'SELL']:
            # Check if this is a new signal (different from last)
            is_new_signal = (
                self.last_signal != signal_data['signal'] or
                self.last_signal_time is None or
                (datetime.now() - self.last_signal_time).total_seconds() > 3600  # 1 hour cooldown
            )

            if is_new_signal:
                # Check daily limits
                limits = self.position_calculator.check_daily_limits(
                    self.trades_today,
                    self.daily_loss
                )

                if not limits['can_trade']:
                    logger.warning(f"Cannot trade: {', '.join(limits['reasons'])}")
                    print(f"\n{Fore.YELLOW}⚠️  Trading limits reached:{Style.RESET_ALL}")
                    for reason in limits['reasons']:
                        print(f"  - {reason}")
                    return

                # Calculate position
                try:
                    position_data = self.position_calculator.calculate_position(
                        signal_data['signal'],
                        signal_data['current_price'],
                        signal_data['atr']
                    )

                    # Validate position
                    validation = self.position_calculator.validate_position(position_data)

                    if not validation['is_valid']:
                        logger.warning(f"Position validation failed: {validation['warnings']}")
                        print(f"\n{Fore.RED}⚠️  Position validation failed:{Style.RESET_ALL}")
                        for warning in validation['warnings']:
                            print(f"  - {warning}")
                        return

                    if validation['warnings']:
                        print(f"\n{Fore.YELLOW}⚠️  Position warnings:{Style.RESET_ALL}")
                        for warning in validation['warnings']:
                            print(f"  - {warning}")

                    # Trigger alert
                    self.alert_system.trigger_alert(signal_data, position_data)

                    # Update state
                    self.last_signal = signal_data['signal']
                    self.last_signal_time = datetime.now()
                    self.trades_today += 1

                except Exception as e:
                    logger.error(f"Error calculating position: {e}")

    def start_monitoring(self):
        """Start continuous monitoring for trading signals"""
        self.monitoring = True
        self.alert_system.send_monitoring_started()

        print(f"\n{Fore.GREEN}✅ Monitoring started. Press Ctrl+C to stop.{Style.RESET_ALL}\n")

        check_interval = self.config['monitoring']['check_interval_minutes'] * 60

        while self.monitoring:
            try:
                self.check_for_signals()

                # Wait for next check
                if self.monitoring:
                    time.sleep(check_interval)

            except KeyboardInterrupt:
                break
            except Exception as e:
                logger.error(f"Error in monitoring loop: {e}")
                self.alert_system.send_error_alert(str(e))
                time.sleep(60)  # Wait a minute before retrying

        self.stop_monitoring()

    def stop_monitoring(self):
        """Stop monitoring"""
        self.monitoring = False
        self.alert_system.send_monitoring_stopped()
        print(f"\n{Fore.YELLOW}Monitoring stopped.{Style.RESET_ALL}")

    def manual_check(self):
        """Perform a manual signal check"""
        print(f"\n{Fore.CYAN}Performing manual analysis...{Style.RESET_ALL}\n")
        self.check_for_signals()

    def view_settings(self):
        """Display current settings"""
        os.system('clear' if os.name == 'posix' else 'cls')
        print(f"\n{Fore.CYAN}═══ CURRENT SETTINGS ═══{Style.RESET_ALL}\n")

        settings_data = [
            ["API Provider", self.config['api']['provider']],
            ["Investment Amount", f"${self.config['trading']['investment_amount']:,.2f}"],
            ["Risk per Trade", f"{self.config['trading']['risk_percentage_per_trade']}%"],
            ["Max Positions/Day", self.config['trading']['max_positions_per_day']],
            ["Daily Loss Limit", f"${self.config['trading']['daily_loss_limit']}"],
            ["Paper Trading", self.config['trading']['paper_trading_mode']],
            ["Check Interval", f"{self.config['monitoring']['check_interval_minutes']} min"],
            ["Notifications", self.config['monitoring']['enable_notifications']],
            ["Min Indicators", self.config['signal_requirements']['min_indicators_confluence']],
        ]

        print(tabulate(settings_data, headers=["Setting", "Value"], tablefmt="grid"))
        print()

    def change_settings(self):
        """Interactive settings change"""
        while True:
            self.view_settings()

            print(f"{Fore.CYAN}What would you like to change?{Style.RESET_ALL}")
            print("1. Investment Amount")
            print("2. Risk Percentage per Trade")
            print("3. Check Interval (minutes)")
            print("4. Paper Trading Mode")
            print("5. Enable/Disable Notifications")
            print("6. Daily Loss Limit")
            print("7. Max Positions per Day")
            print("0. Back to main menu")

            choice = input(f"\n{Fore.YELLOW}Enter choice: {Style.RESET_ALL}").strip()

            try:
                if choice == '1':
                    amount = float(input("Enter investment amount: $"))
                    self.config['trading']['investment_amount'] = amount
                    self.position_calculator.adjust_for_account_balance(amount)
                elif choice == '2':
                    risk = float(input("Enter risk percentage (1-5): "))
                    if 0 < risk <= 5:
                        self.config['trading']['risk_percentage_per_trade'] = risk
                    else:
                        print(f"{Fore.RED}Risk must be between 0 and 5%{Style.RESET_ALL}")
                        continue
                elif choice == '3':
                    interval = int(input("Enter check interval in minutes (1-60): "))
                    if 1 <= interval <= 60:
                        self.config['monitoring']['check_interval_minutes'] = interval
                    else:
                        print(f"{Fore.RED}Interval must be between 1 and 60 minutes{Style.RESET_ALL}")
                        continue
                elif choice == '4':
                    mode = input("Enable paper trading? (yes/no): ").lower()
                    self.config['trading']['paper_trading_mode'] = mode.startswith('y')
                elif choice == '5':
                    enable = input("Enable notifications? (yes/no): ").lower()
                    self.config['monitoring']['enable_notifications'] = enable.startswith('y')
                elif choice == '6':
                    limit = float(input("Enter daily loss limit: $"))
                    self.config['trading']['daily_loss_limit'] = limit
                elif choice == '7':
                    max_pos = int(input("Enter max positions per day (1-10): "))
                    if 1 <= max_pos <= 10:
                        self.config['trading']['max_positions_per_day'] = max_pos
                    else:
                        print(f"{Fore.RED}Max positions must be between 1 and 10{Style.RESET_ALL}")
                        continue
                elif choice == '0':
                    break
                else:
                    print(f"{Fore.RED}Invalid choice{Style.RESET_ALL}")
                    continue

                self.save_config()
                print(f"{Fore.GREEN}✅ Settings updated successfully!{Style.RESET_ALL}")
                time.sleep(1)

            except ValueError:
                print(f"{Fore.RED}Invalid input. Please try again.{Style.RESET_ALL}")
                time.sleep(2)

    def view_alert_history(self):
        """Display recent alert history"""
        os.system('clear' if os.name == 'posix' else 'cls')
        print(f"\n{Fore.CYAN}═══ RECENT ALERTS ═══{Style.RESET_ALL}\n")

        alerts = self.alert_system.get_recent_alerts(limit=10)

        if not alerts:
            print("No alerts found.")
            return

        # Format alerts for display
        alert_data = []
        for alert in alerts[-10:]:  # Last 10 alerts
            timestamp = datetime.fromisoformat(alert['Timestamp'])
            alert_data.append([
                timestamp.strftime('%Y-%m-%d %H:%M'),
                alert['Signal'],
                f"${float(alert['Entry_Price']):.2f}",
                f"${float(alert['Stop_Loss']):.2f}",
                f"{float(alert['Lot_Size']):.2f}",
                f"{float(alert['Confidence']):.0f}%"
            ])

        print(tabulate(
            alert_data,
            headers=['Time', 'Signal', 'Entry', 'Stop Loss', 'Lots', 'Confidence'],
            tablefmt='grid'
        ))
        print()

    def main_menu(self):
        """Display and handle main menu"""
        while True:
            os.system('clear' if os.name == 'posix' else 'cls')
            self.display_banner()

            print(f"\n{Fore.CYAN}═══ MAIN MENU ═══{Style.RESET_ALL}\n")
            print("1. 🚀 Start Monitoring")
            print("2. 🔍 Manual Signal Check")
            print("3. ⚙️  View/Change Settings")
            print("4. 📊 View Alert History")
            print("5. 📈 View Current Trend")
            print("6. 🧹 Clear Old Alerts")
            print("0. 🚪 Exit")

            choice = input(f"\n{Fore.YELLOW}Enter your choice: {Style.RESET_ALL}").strip()

            if choice == '1':
                self.start_monitoring()
            elif choice == '2':
                self.manual_check()
                input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
            elif choice == '3':
                self.change_settings()
            elif choice == '4':
                self.view_alert_history()
                input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
            elif choice == '5':
                self.show_trend_analysis()
                input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
            elif choice == '6':
                days = input("Clear alerts older than how many days? (default 30): ")
                days = int(days) if days.strip() else 30
                self.alert_system.clear_old_alerts(days)
                print(f"{Fore.GREEN}✅ Old alerts cleared!{Style.RESET_ALL}")
                time.sleep(2)
            elif choice == '0':
                print(f"\n{Fore.CYAN}Thank you for using Forex Trading Assistant!{Style.RESET_ALL}")
                sys.exit(0)
            else:
                print(f"{Fore.RED}Invalid choice. Please try again.{Style.RESET_ALL}")
                time.sleep(1)

    def show_trend_analysis(self):
        """Display detailed trend analysis"""
        os.system('clear' if os.name == 'posix' else 'cls')
        print(f"\n{Fore.CYAN}═══ TREND ANALYSIS ═══{Style.RESET_ALL}\n")

        try:
            # Fetch and analyze data
            historical_data = self.data_fetcher.update_historical_data(days=30, interval='1h')

            if historical_data is None:
                print(f"{Fore.RED}Failed to fetch data{Style.RESET_ALL}")
                return

            historical_data = self.indicators.calculate_all_indicators(historical_data)
            trend = self.indicators.get_current_trend(historical_data)

            latest = historical_data.iloc[-1]

            print(f"Current Trend: {Fore.YELLOW}{trend}{Style.RESET_ALL}\n")
            print(f"Price: ${latest['Close']:.2f}")
            print(f"SMA 20: ${latest['SMA_20']:.2f}")
            print(f"SMA 50: ${latest['SMA_50']:.2f}")
            print(f"SMA 200: ${latest['SMA_200']:.2f}")
            print(f"\nRSI: {latest['RSI']:.2f}")
            print(f"MACD: {latest['MACD']:.4f}")
            print(f"MACD Signal: {latest['MACD_Signal']:.4f}")
            print(f"\nBollinger Upper: ${latest['BB_Upper']:.2f}")
            print(f"Bollinger Middle: ${latest['BB_Middle']:.2f}")
            print(f"Bollinger Lower: ${latest['BB_Lower']:.2f}")
            print(f"\nATR: {latest['ATR']:.2f}")

            # Support and Resistance
            levels = self.indicators.find_support_resistance(historical_data)
            if levels['support']:
                print(f"\nSupport Levels: {', '.join([f'${s:.2f}' for s in levels['support']])}")
            if levels['resistance']:
                print(f"Resistance Levels: {', '.join([f'${r:.2f}' for r in levels['resistance']])}")

        except Exception as e:
            logger.error(f"Error in trend analysis: {e}")
            print(f"{Fore.RED}Error performing trend analysis: {e}{Style.RESET_ALL}")


def main():
    """Main entry point"""
    try:
        app = ForexTradingAssistant()
        app.main_menu()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Exiting...{Style.RESET_ALL}")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        print(f"{Fore.RED}Fatal error: {e}{Style.RESET_ALL}")
        sys.exit(1)


if __name__ == '__main__':
    main()
