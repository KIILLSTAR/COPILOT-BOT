"""
Trade Configuration - All tunable parameters in one place
"""
from config.safety_config import safety

# === Safety (always first) ===
DRY_RUN = True  # Hardcoded True until you explicitly enable live trading
AUTO_MODE = False  # True = auto-execute signals, False = manual approval

# === Jupiter Perpetuals ===
# Supported: ETH-PERP, SOL-PERP, BTC-PERP (Jupiter perps on Solana)
TRADING_PAIR = "ETH-PERP"

# === Risk Management ===
TRADE_SIZE_USD   = 100    # Base trade size in USD
LEVERAGE         = 2      # Leverage multiplier (2x default for safety)
STOP_LOSS_PCT    = 0.02   # 2% stop loss
TAKE_PROFIT_PCT  = 0.04   # 4% take profit
MAX_LOSS_THRESHOLD   = 50.0   # Auto-close if total loss exceeds this
MAX_DAILY_TRADES     = 10
AUTO_CLOSE_ENABLED   = True

# === Signal Detection ===
SIGNAL_THRESHOLD = 0.65   # Minimum confidence score to trigger a trade (0-1)

# === Timing ===
CYCLE_DELAY_SECONDS = 60  # How often the bot checks for signals

# === Logging ===
LOG_FILE = "data/trade_log.txt"
VERBOSE  = False
