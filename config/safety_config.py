"""
Safety Configuration - CRITICAL PROTECTION LAYER
Multiple safeguards to prevent accidental live trading
"""
import os

class SafetyConfig:
    SAFETY_LOCK_ENABLED = True
    MAX_DAILY_TRADES = 10
    MAX_TRADE_SIZE_USD = 500
    MAX_TOTAL_EXPOSURE_USD = 2000

    @classmethod
    def is_dry_run_forced(cls) -> bool:
        if cls.SAFETY_LOCK_ENABLED:
            return True
        if os.getenv('ENABLE_LIVE_TRADING', 'FALSE').upper() != 'TRUE':
            return True
        if not os.path.exists('.live_trading_confirmed'):
            return True
        if os.getenv('WALLET_APPROVED_LIVE_TRADING', 'FALSE').upper() != 'TRUE':
            return True
        return False

    @classmethod
    def get_safety_status(cls) -> dict:
        return {
            "forced_dry_run": cls.is_dry_run_forced(),
            "safety_lock": cls.SAFETY_LOCK_ENABLED,
            "env_check": os.getenv('ENABLE_LIVE_TRADING', 'FALSE').upper() == 'TRUE',
            "manual_file": os.path.exists('.live_trading_confirmed'),
            "wallet_approved": os.getenv('WALLET_APPROVED_LIVE_TRADING', 'FALSE').upper() == 'TRUE',
            "max_trade_size": cls.MAX_TRADE_SIZE_USD,
            "max_exposure": cls.MAX_TOTAL_EXPOSURE_USD
        }

safety = SafetyConfig()
