"""
Safety Configuration - CRITICAL PROTECTION LAYER
Multiple safeguards to prevent accidental live trading
"""
import os
from typing import Literal

class SafetyConfig:
    """
    Immutable safety configuration with multiple protection layers
    """
    
    # CRITICAL: Primary safety lock - can only be changed manually in code
    SAFETY_LOCK_ENABLED = True  # NEVER set to False unless you want live trading
    
    # Multiple confirmation layers
    REQUIRE_MANUAL_CONFIRMATION = True
    REQUIRE_ENVIRONMENT_VARIABLE = True
    REQUIRE_WALLET_CONFIRMATION = True
    
    # Safety limits even if live trading is enabled
    MAX_DAILY_TRADES = 5
    MAX_TRADE_SIZE_USD = 50  # Maximum $50 per trade
    MAX_TOTAL_EXPOSURE_USD = 200  # Maximum $200 total exposure
    
    @classmethod
    def is_dry_run_forced(cls) -> bool:
        """
        Check if dry run is forced by safety mechanisms
        Returns True if ANY safety mechanism forces dry run
        """
        # Layer 1: Primary safety lock
        if cls.SAFETY_LOCK_ENABLED:
            return True
            
        # Layer 2: Environment variable check
        if cls.REQUIRE_ENVIRONMENT_VARIABLE:
            live_trading_enabled = os.getenv('ENABLE_LIVE_TRADING', 'FALSE').upper()
            if live_trading_enabled != 'TRUE':
                return True
        
        # Layer 3: Manual confirmation file check
        if cls.REQUIRE_MANUAL_CONFIRMATION:
            if not os.path.exists('.live_trading_confirmed'):
                return True
        
        # Layer 4: Wallet safety check
        if cls.REQUIRE_WALLET_CONFIRMATION:
            wallet_approved = os.getenv('WALLET_APPROVED_LIVE_TRADING', 'FALSE').upper()
            if wallet_approved != 'TRUE':
                return True
        
        return False
    
    @classmethod
    def get_safety_status(cls) -> dict:
        """Get detailed safety status"""
        return {
            "forced_dry_run": cls.is_dry_run_forced(),
            "safety_lock": cls.SAFETY_LOCK_ENABLED,
            "env_check": os.getenv('ENABLE_LIVE_TRADING', 'FALSE').upper() == 'TRUE',
            "manual_file": os.path.exists('.live_trading_confirmed'),
            "wallet_approved": os.getenv('WALLET_APPROVED_LIVE_TRADING', 'FALSE').upper() == 'TRUE',
            "max_trade_size": cls.MAX_TRADE_SIZE_USD,
            "max_exposure": cls.MAX_TOTAL_EXPOSURE_USD
        }
    
    @classmethod
    def print_safety_status(cls):
        """Print detailed safety status"""
        status = cls.get_safety_status()
        
        print("🔒 SAFETY STATUS")
        print("=" * 40)
        print(f"Mode: {'🧪 DRY RUN (SAFE)' if status['forced_dry_run'] else '🔴 LIVE TRADING'}")
        print(f"Safety Lock: {'🔒 ENABLED' if status['safety_lock'] else '⚠️ DISABLED'}")
        print(f"Environment: {'✅ LIVE ENABLED' if status['env_check'] else '🔒 BLOCKED'}")
        print(f"Manual File: {'✅ EXISTS' if status['manual_file'] else '🔒 MISSING'}")
        print(f"Wallet Approved: {'✅ YES' if status['wallet_approved'] else '🔒 NO'}")
        print(f"Max Trade Size: ${status['max_trade_size']}")
        print(f"Max Exposure: ${status['max_exposure']}")
        print()
        
        if status['forced_dry_run']:
            print("💚 YOUR FUNDS ARE SAFE - DRY RUN MODE ACTIVE")
        else:
            print("⚠️ WARNING: LIVE TRADING IS POSSIBLE")
        print()

# Global safety instance
safety = SafetyConfig()