"""
Consolidated Configuration File
Combines all configuration settings from various modules
"""
import os
import json
from typing import Literal

# =============================================================================
# SAFETY CONFIGURATION - CRITICAL PROTECTION LAYER
# =============================================================================

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

# =============================================================================
# TRADING CONFIGURATION
# =============================================================================

# CRITICAL SAFETY CHECK - This FORCES dry run mode if ANY safety mechanism is active
FORCED_DRY_RUN = safety.is_dry_run_forced()

# Mode Toggles
DRY_RUN = True or FORCED_DRY_RUN  # ALWAYS True if safety is enabled
AUTO_MODE = False      # True = auto-confirm trades, False = manual confirmation

# Safety override check
if not DRY_RUN and FORCED_DRY_RUN:
    DRY_RUN = True  # Force dry run for safety

# Strategy Parameters
SIGNAL_THRESHOLD = 0.75  # Minimum confidence to trigger a signal

# Risk Management
TRADE_SIZE_USD = 100    # Default trade size in USD
LEVERAGE = 1           # Leverage multiplier for perps
PNL_ALERT_THRESHOLD = 20.0   # Alert when profit exceeds this
MAX_LOSS_THRESHOLD = 50.0    # Max loss before auto-close
AUTO_CLOSE_ENABLED = True    # Enable automatic position closing

# Timing
CYCLE_DELAY_SECONDS = 60    # Delay between trading cycles

# Logging
LOG_FILE = "trade_log.txt"
VERBOSE = False             # Enable detailed logging

# =============================================================================
# WALLET CONFIGURATION
# =============================================================================

# List of supported tokens for signal detection and trading
TOKEN_LIST = [
    "SOL",
    "USDC",
    "BONK",
    "JUP",
    "ETH",
    "BTC",
    "RAY",
    "SRM"
]

# Metadata for each token: mint address, decimals, display name
TOKEN_META = {
    "SOL": {
        "mint": "So11111111111111111111111111111111111111112",
        "decimals": 9,
        "name": "Solana"
    },
    "USDC": {
        "mint": "EPjFWdd5AufqSSqeM2qAqAqAqAqAqAqAqAqAqAqAqA",
        "decimals": 6,
        "name": "USD Coin"
    },
    "BONK": {
        "mint": "DezX3zY3Z3Z3Z3Z3Z3Z3Z3Z3Z3Z3Z3Z3Z3Z3Z3Z3Z3Z3",
        "decimals": 5,
        "name": "Bonk"
    },
    "JUP": {
        "mint": "JUPZ3Z3Z3Z3Z3Z3Z3Z3Z3Z3Z3Z3Z3Z3Z3Z3Z3Z3Z3Z3",
        "decimals": 6,
        "name": "Jupiter"
    },
    "ETH": {
        "mint": "7vfCXTUXx5WJV5JADk17DUJ4ksgau7utNKj4b963voxs",
        "decimals": 8,
        "name": "Ethereum (Wormhole)"
    },
    "BTC": {
        "mint": "BTCmintAddressHere",
        "decimals": 8,
        "name": "Bitcoin (Wormhole)"
    },
    "RAY": {
        "mint": "4k3Dyjzvzp8e2Y2X2X2X2X2X2X2X2X2X2X2X2X2X2X2",
        "decimals": 6,
        "name": "Raydium"
    },
    "SRM": {
        "mint": "SRMmintAddressHere",
        "decimals": 6,
        "name": "Serum"
    }
}

# Utility functions for token metadata
def get_token_mint(token_symbol: str) -> str:
    return TOKEN_META.get(token_symbol, {}).get("mint", "")

def get_token_decimals(token_symbol: str) -> int:
    return TOKEN_META.get(token_symbol, {}).get("decimals", 0)

# =============================================================================
# SAFE WALLET MANAGER CONFIGURATION
# =============================================================================

MIN_BALANCE_THRESHOLD = 0.01
LOG_PATH = "./logs/"

# =============================================================================
# UTILS CONFIGURATION
# =============================================================================

CONFIG_PATH = "utils/config.json"

def load_config():
    """Load configuration from JSON file"""
    if not os.path.exists(CONFIG_PATH):
        return {"mode": "manual"}
    with open(CONFIG_PATH, "r") as f:
        return json.load(f)

def save_config(data):
    """Save configuration to JSON file"""
    with open(CONFIG_PATH, "w") as f:
        json.dump(data, f, indent=2)

# =============================================================================
# BACKWARD COMPATIBILITY
# =============================================================================

# For backward compatibility with existing imports
trade_config = type('TradeConfig', (), {
    'DRY_RUN': DRY_RUN,
    'AUTO_MODE': AUTO_MODE,
    'SIGNAL_THRESHOLD': SIGNAL_THRESHOLD,
    'TRADE_SIZE_USD': TRADE_SIZE_USD,
    'LEVERAGE': LEVERAGE,
    'PNL_ALERT_THRESHOLD': PNL_ALERT_THRESHOLD,
    'MAX_LOSS_THRESHOLD': MAX_LOSS_THRESHOLD,
    'AUTO_CLOSE_ENABLED': AUTO_CLOSE_ENABLED,
    'CYCLE_DELAY_SECONDS': CYCLE_DELAY_SECONDS,
    'LOG_FILE': LOG_FILE,
    'VERBOSE': VERBOSE,
})()

safety_config = type('SafetyConfig', (), {
    'safety': safety,
    'SafetyConfig': SafetyConfig,
})()

# Make all exports available
__all__ = [
    'SafetyConfig', 'safety', 'DRY_RUN', 'AUTO_MODE', 'SIGNAL_THRESHOLD',
    'TRADE_SIZE_USD', 'LEVERAGE', 'PNL_ALERT_THRESHOLD', 'MAX_LOSS_THRESHOLD',
    'AUTO_CLOSE_ENABLED', 'CYCLE_DELAY_SECONDS', 'LOG_FILE', 'VERBOSE',
    'TOKEN_LIST', 'TOKEN_META', 'get_token_mint', 'get_token_decimals',
    'MIN_BALANCE_THRESHOLD', 'LOG_PATH', 'CONFIG_PATH', 'load_config', 'save_config',
    'trade_config', 'safety_config'
]