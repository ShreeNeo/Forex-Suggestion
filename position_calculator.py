"""
Position Calculator Module for Forex Trading Assistant
Handles position sizing, risk management, and trade calculations
"""

import logging
from typing import Dict

logger = logging.getLogger(__name__)


class PositionCalculator:
    """Calculate position sizes and risk management parameters"""

    def __init__(self, config: Dict):
        self.config = config
        self.trading_config = config.get('trading', {})
        self.risk_config = config.get('risk_management', {})

        self.investment_amount = self.trading_config.get('investment_amount', 10000)
        self.risk_percentage = self.trading_config.get('risk_percentage_per_trade', 1.5)
        self.leverage = self.trading_config.get('leverage', 100)

        # Gold specific constants
        self.oz_per_lot = 100  # Standard gold contract is 100 troy ounces
        self.pip_value = 0.01  # For gold, 1 pip = $0.01 per ounce

    def calculate_position(self, signal: str, current_price: float, atr: float) -> Dict:
        """
        Calculate complete position sizing and risk management parameters

        Args:
            signal: 'BUY' or 'SELL'
            current_price: Current market price
            atr: Average True Range for volatility-based stop loss

        Returns:
            Dictionary with all position details
        """
        try:
            # Calculate risk amount in dollars
            risk_amount = self.investment_amount * (self.risk_percentage / 100)

            # Calculate stop loss based on ATR
            stop_loss_multiplier = self.risk_config.get('stop_loss_atr_multiplier', 2)
            stop_loss_distance = atr * stop_loss_multiplier

            # Determine entry price (could add some buffer)
            entry_price = current_price

            # Calculate stop loss price based on signal direction
            if signal == 'BUY':
                stop_loss = entry_price - stop_loss_distance
            else:  # SELL
                stop_loss = entry_price + stop_loss_distance

            # Calculate stop loss in pips
            stop_loss_pips = abs(entry_price - stop_loss) / self.pip_value

            # Calculate position size
            # Risk amount = Position size in oz * Stop loss distance
            # Position size in oz = Risk amount / Stop loss distance
            position_size_oz = risk_amount / stop_loss_distance

            # Convert to lots (1 lot = 100 oz for gold)
            lot_size = position_size_oz / self.oz_per_lot

            # Calculate take profit levels
            risk_reward_ratio = self.risk_config.get('risk_reward_ratio_min', 2)
            tp1_ratio = self.risk_config.get('take_profit_1_ratio', 1.5)
            tp2_ratio = self.risk_config.get('take_profit_2_ratio', 3)

            if signal == 'BUY':
                take_profit_1 = entry_price + (stop_loss_distance * tp1_ratio)
                take_profit_2 = entry_price + (stop_loss_distance * tp2_ratio)
            else:  # SELL
                take_profit_1 = entry_price - (stop_loss_distance * tp1_ratio)
                take_profit_2 = entry_price - (stop_loss_distance * tp2_ratio)

            # Calculate pips for take profit levels
            tp1_pips = abs(take_profit_1 - entry_price) / self.pip_value
            tp2_pips = abs(take_profit_2 - entry_price) / self.pip_value

            # Calculate potential profits
            potential_profit_tp1 = position_size_oz * abs(take_profit_1 - entry_price)
            potential_profit_tp2 = position_size_oz * abs(take_profit_2 - entry_price)

            # Calculate required margin (for informational purposes)
            position_value = position_size_oz * entry_price
            required_margin = position_value / self.leverage

            position_details = {
                'signal': signal,
                'entry_price': round(entry_price, 2),
                'stop_loss': round(stop_loss, 2),
                'take_profit_1': round(take_profit_1, 2),
                'take_profit_2': round(take_profit_2, 2),
                'stop_loss_pips': round(stop_loss_pips, 1),
                'tp1_pips': round(tp1_pips, 1),
                'tp2_pips': round(tp2_pips, 1),
                'lot_size': round(lot_size, 2),
                'ounces': round(position_size_oz, 3),
                'risk_amount': round(risk_amount, 2),
                'risk_reward_ratio': round(tp2_ratio, 2),
                'potential_profit_tp1': round(potential_profit_tp1, 2),
                'potential_profit_tp2': round(potential_profit_tp2, 2),
                'required_margin': round(required_margin, 2),
                'position_value': round(position_value, 2),
                'atr': round(atr, 2)
            }

            logger.info(f"Position calculated: {signal} {lot_size:.2f} lots at ${entry_price:.2f}")
            return position_details

        except Exception as e:
            logger.error(f"Error calculating position: {e}")
            raise

    def validate_position(self, position: Dict) -> Dict:
        """
        Validate position against risk management rules

        Returns:
            Dictionary with validation results and warnings
        """
        warnings = []
        is_valid = True

        # Check if lot size is within reasonable limits
        if position['lot_size'] < 0.01:
            warnings.append("Position size too small (< 0.01 lots)")
            is_valid = False
        elif position['lot_size'] > 10:
            warnings.append("Position size very large (> 10 lots) - verify before trading")

        # Check if risk amount is reasonable
        max_risk = self.investment_amount * 0.05  # 5% hard limit
        if position['risk_amount'] > max_risk:
            warnings.append(f"Risk amount exceeds 5% of capital (${max_risk:.2f})")
            is_valid = False

        # Check margin requirements
        if position['required_margin'] > self.investment_amount * 0.5:
            warnings.append("Required margin exceeds 50% of capital - high leverage risk")

        # Check stop loss distance
        if position['stop_loss_pips'] < 10:
            warnings.append("Stop loss very tight (< 10 pips) - may get stopped out easily")
        elif position['stop_loss_pips'] > 500:
            warnings.append("Stop loss very wide (> 500 pips) - consider reducing risk")

        return {
            'is_valid': is_valid,
            'warnings': warnings
        }

    def calculate_pip_value(self, lot_size: float) -> float:
        """Calculate pip value for given lot size"""
        # For gold: 1 pip = $0.01 per ounce
        # Pip value = lot_size * oz_per_lot * pip_value
        return lot_size * self.oz_per_lot * self.pip_value

    def calculate_profit_loss(self, entry_price: float, exit_price: float,
                             lot_size: float, signal: str) -> float:
        """
        Calculate profit/loss for a trade

        Args:
            entry_price: Entry price
            exit_price: Exit price
            lot_size: Position size in lots
            signal: 'BUY' or 'SELL'

        Returns:
            Profit/loss in dollars
        """
        position_size_oz = lot_size * self.oz_per_lot

        if signal == 'BUY':
            profit_loss = position_size_oz * (exit_price - entry_price)
        else:  # SELL
            profit_loss = position_size_oz * (entry_price - exit_price)

        return round(profit_loss, 2)

    def adjust_for_account_balance(self, current_balance: float):
        """Update investment amount based on current account balance"""
        self.investment_amount = current_balance
        logger.info(f"Investment amount updated to ${current_balance:.2f}")

    def calculate_daily_loss_limit(self) -> float:
        """Calculate maximum allowed daily loss"""
        daily_loss_limit = self.trading_config.get('daily_loss_limit', 300)
        return min(daily_loss_limit, self.investment_amount * 0.05)  # Max 5% per day

    def check_daily_limits(self, trades_today: int, losses_today: float) -> Dict:
        """
        Check if daily limits have been reached

        Args:
            trades_today: Number of trades taken today
            losses_today: Total losses today (positive number)

        Returns:
            Dictionary with limit status
        """
        max_positions = self.trading_config.get('max_positions_per_day', 3)
        max_daily_loss = self.calculate_daily_loss_limit()

        can_trade = True
        reasons = []

        if trades_today >= max_positions:
            can_trade = False
            reasons.append(f"Daily position limit reached ({max_positions} trades)")

        if losses_today >= max_daily_loss:
            can_trade = False
            reasons.append(f"Daily loss limit reached (${max_daily_loss:.2f})")

        return {
            'can_trade': can_trade,
            'reasons': reasons,
            'trades_today': trades_today,
            'max_positions': max_positions,
            'losses_today': losses_today,
            'max_daily_loss': max_daily_loss
        }

    def format_position_summary(self, position: Dict) -> str:
        """Format position details as a readable string"""
        summary = f"""
Position Summary:
─────────────────────────────────────────────
Signal: {position['signal']}
Entry Price: ${position['entry_price']:.2f}
Stop Loss: ${position['stop_loss']:.2f} ({position['stop_loss_pips']:.1f} pips)
Take Profit 1: ${position['take_profit_1']:.2f} ({position['tp1_pips']:.1f} pips)
Take Profit 2: ${position['take_profit_2']:.2f} ({position['tp2_pips']:.1f} pips)

Position Size: {position['lot_size']:.2f} lots ({position['ounces']:.3f} oz)
Risk Amount: ${position['risk_amount']:.2f}
Potential Profit (TP1): ${position['potential_profit_tp1']:.2f}
Potential Profit (TP2): ${position['potential_profit_tp2']:.2f}
Risk/Reward Ratio: 1:{position['risk_reward_ratio']:.1f}

Margin Required: ${position['required_margin']:.2f}
Position Value: ${position['position_value']:.2f}
─────────────────────────────────────────────
"""
        return summary
