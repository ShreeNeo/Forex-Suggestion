"""
Alert System Module for Forex Trading Assistant
Handles notifications, logging, and alert management
"""

import os
import logging
from datetime import datetime
from typing import Dict, Optional
import json
import csv

try:
    from plyer import notification
    NOTIFICATIONS_AVAILABLE = True
except ImportError:
    NOTIFICATIONS_AVAILABLE = False
    logging.warning("plyer not available - desktop notifications disabled")

logger = logging.getLogger(__name__)


class AlertSystem:
    """Manage trading alerts and notifications"""

    def __init__(self, config: Dict):
        self.config = config
        self.monitoring_config = config.get('monitoring', {})
        self.alert_log_file = config.get('data_storage', {}).get('alert_log_file', 'data/alert_log.csv')
        self.enable_notifications = self.monitoring_config.get('enable_notifications', True)
        self.notification_sound = self.monitoring_config.get('notification_sound', True)
        self.log_alerts = self.monitoring_config.get('log_alerts', True)

        # Create data directory if it doesn't exist
        os.makedirs(os.path.dirname(self.alert_log_file), exist_ok=True)

        # Initialize alert log file if it doesn't exist
        self._initialize_alert_log()

    def _initialize_alert_log(self):
        """Create alert log file with headers if it doesn't exist"""
        if not os.path.exists(self.alert_log_file):
            with open(self.alert_log_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([
                    'Timestamp',
                    'Signal',
                    'Price',
                    'Entry_Price',
                    'Stop_Loss',
                    'Take_Profit_1',
                    'Take_Profit_2',
                    'Lot_Size',
                    'Risk_Amount',
                    'Risk_Reward_Ratio',
                    'Confidence',
                    'Reasons'
                ])

    def send_desktop_notification(self, title: str, message: str, timeout: int = 10):
        """Send desktop notification"""
        if not self.enable_notifications:
            return

        if not NOTIFICATIONS_AVAILABLE:
            logger.warning("Desktop notifications not available")
            return

        try:
            notification.notify(
                title=title,
                message=message,
                app_name='Forex Trading Assistant',
                timeout=timeout
            )
            logger.info(f"Desktop notification sent: {title}")
        except Exception as e:
            logger.error(f"Failed to send desktop notification: {e}")

    def log_alert(self, alert_data: Dict):
        """Log alert to CSV file"""
        if not self.log_alerts:
            return

        try:
            with open(self.alert_log_file, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([
                    alert_data.get('timestamp', datetime.now().isoformat()),
                    alert_data.get('signal', 'N/A'),
                    alert_data.get('current_price', 0),
                    alert_data.get('entry_price', 0),
                    alert_data.get('stop_loss', 0),
                    alert_data.get('take_profit_1', 0),
                    alert_data.get('take_profit_2', 0),
                    alert_data.get('lot_size', 0),
                    alert_data.get('risk_amount', 0),
                    alert_data.get('risk_reward_ratio', 0),
                    alert_data.get('confidence', 0),
                    '; '.join(alert_data.get('reasons', []))
                ])
            logger.info(f"Alert logged to {self.alert_log_file}")
        except Exception as e:
            logger.error(f"Failed to log alert: {e}")

    def trigger_alert(self, signal_data: Dict, position_data: Dict):
        """
        Trigger a trading alert with all relevant information

        Args:
            signal_data: Dictionary containing signal information from indicators
            position_data: Dictionary containing position sizing and risk management data
        """
        timestamp = datetime.now()

        # Format alert message
        alert_message = self._format_alert_message(signal_data, position_data, timestamp)

        # Print to console
        print("\n" + "="*70)
        print(alert_message)
        print("="*70 + "\n")

        # Send desktop notification
        notification_title = f"🚨 {signal_data['signal']} SIGNAL - XAU/USD"
        notification_body = (
            f"Entry: ${position_data['entry_price']:.2f} | "
            f"SL: ${position_data['stop_loss']:.2f} | "
            f"TP1: ${position_data['take_profit_1']:.2f} | "
            f"Confidence: {signal_data['confidence']:.0f}%"
        )
        self.send_desktop_notification(notification_title, notification_body)

        # Log to file
        alert_log_data = {
            'timestamp': timestamp.isoformat(),
            'signal': signal_data['signal'],
            'current_price': signal_data['current_price'],
            'entry_price': position_data['entry_price'],
            'stop_loss': position_data['stop_loss'],
            'take_profit_1': position_data['take_profit_1'],
            'take_profit_2': position_data['take_profit_2'],
            'lot_size': position_data['lot_size'],
            'risk_amount': position_data['risk_amount'],
            'risk_reward_ratio': position_data['risk_reward_ratio'],
            'confidence': signal_data['confidence'],
            'reasons': signal_data['reasons']
        }
        self.log_alert(alert_log_data)

        return alert_log_data

    def _format_alert_message(self, signal_data: Dict, position_data: Dict, timestamp: datetime) -> str:
        """Format a detailed alert message"""
        signal_emoji = "📈" if signal_data['signal'] == 'BUY' else "📉"

        message = f"""
{signal_emoji} TRADING SIGNAL DETECTED {signal_emoji}
Time: {timestamp.strftime('%Y-%m-%d %H:%M:%S')}

ACTION: {signal_data['signal']}
Confidence: {signal_data['confidence']:.1f}% ({signal_data['strength']}/6 indicators)

PRICE INFORMATION:
├─ Current Price: ${signal_data['current_price']:.2f}
├─ Entry Price: ${position_data['entry_price']:.2f}
├─ Stop Loss: ${position_data['stop_loss']:.2f} ({position_data['stop_loss_pips']:.1f} pips)
├─ Take Profit 1: ${position_data['take_profit_1']:.2f} ({position_data['tp1_pips']:.1f} pips)
└─ Take Profit 2: ${position_data['take_profit_2']:.2f} ({position_data['tp2_pips']:.1f} pips)

POSITION SIZING:
├─ Lot Size: {position_data['lot_size']:.2f} lots
├─ Ounces: {position_data['ounces']:.3f} oz
├─ Risk Amount: ${position_data['risk_amount']:.2f}
├─ Risk/Reward Ratio: 1:{position_data['risk_reward_ratio']:.2f}
└─ Potential Profit (TP1): ${position_data['potential_profit_tp1']:.2f}

TECHNICAL INDICATORS:
├─ RSI: {signal_data['rsi']:.2f}
├─ MACD: {signal_data['macd']:.4f}
└─ ATR: {signal_data['atr']:.2f}

REASONS FOR SIGNAL:
"""
        for i, reason in enumerate(signal_data['reasons'], 1):
            message += f"{i}. {reason}\n"

        message += f"\n⚠️  DISCLAIMER: This is {self.config.get('trading', {}).get('paper_trading_mode') and 'PAPER TRADING' or 'LIVE TRADING'} mode"

        return message

    def send_price_alert(self, current_price: float, change_24h: float):
        """Send simple price update notification"""
        change_emoji = "📈" if change_24h > 0 else "📉"
        title = f"{change_emoji} XAU/USD Price Update"
        message = f"Current: ${current_price:.2f} | 24h Change: {change_24h:+.2f}%"

        self.send_desktop_notification(title, message, timeout=5)

    def send_error_alert(self, error_message: str):
        """Send error notification"""
        title = "⚠️ Forex Trading Bot Error"
        self.send_desktop_notification(title, error_message, timeout=10)

    def send_monitoring_started(self):
        """Notify that monitoring has started"""
        title = "✅ Forex Trading Bot Started"
        message = "Monitoring XAU/USD for trading opportunities"
        self.send_desktop_notification(title, message, timeout=5)

    def send_monitoring_stopped(self):
        """Notify that monitoring has stopped"""
        title = "🛑 Forex Trading Bot Stopped"
        message = "Monitoring has been stopped"
        self.send_desktop_notification(title, message, timeout=5)

    def get_recent_alerts(self, limit: int = 10) -> list:
        """Retrieve recent alerts from log file"""
        alerts = []

        if not os.path.exists(self.alert_log_file):
            return alerts

        try:
            with open(self.alert_log_file, 'r') as f:
                reader = csv.DictReader(f)
                alerts = list(reader)

            # Return most recent alerts
            return alerts[-limit:] if len(alerts) > limit else alerts

        except Exception as e:
            logger.error(f"Failed to read alert log: {e}")
            return []

    def clear_old_alerts(self, days: int = 30):
        """Clear alerts older than specified days"""
        if not os.path.exists(self.alert_log_file):
            return

        try:
            alerts = []
            cutoff_date = datetime.now().timestamp() - (days * 24 * 60 * 60)

            with open(self.alert_log_file, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    alert_time = datetime.fromisoformat(row['Timestamp']).timestamp()
                    if alert_time > cutoff_date:
                        alerts.append(row)

            # Rewrite file with only recent alerts
            with open(self.alert_log_file, 'w', newline='') as f:
                if alerts:
                    writer = csv.DictWriter(f, fieldnames=alerts[0].keys())
                    writer.writeheader()
                    writer.writerows(alerts)

            logger.info(f"Cleared alerts older than {days} days")

        except Exception as e:
            logger.error(f"Failed to clear old alerts: {e}")
