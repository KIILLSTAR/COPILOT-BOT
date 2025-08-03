# config/trade_config.py

# Import safety configuration first
from config.safety_config import safety

# === CRITICAL SAFETY CHECK ===
# This FORCES dry run mode if ANY safety mechanism is active
FORCED_DRY_RUN = safety.is_dry_run_forced()

# === Mode Toggles ===
# DRY_RUN is now controlled by safety mechanisms
DRY_RUN = True or FORCED_DRY_RUN  # ALWAYS True if safety is enabled
AUTO_MODE = False      # True = auto-confirm trades, False = manual confirmation

# Safety override check
if not DRY_RUN and FORCED_DRY_RUN:
    DRY_RUN = True  # Force dry run for safety

# === Strategy Parameters ===
SIGNAL_THRESHOLD = 0.75  # Minimum confidence to trigger a signal

# === Risk Management ===
TRADE_SIZE_USD = 100    # Default trade size in USD
LEVERAGE = 1           # Leverage multiplier for perps
PNL_ALERT_THRESHOLD = 20.0   # Alert when profit exceeds this
MAX_LOSS_THRESHOLD = 50.0    # Max loss before auto-close
AUTO_CLOSE_ENABLED = True    # Enable automatic position closing

# === Timing ===
CYCLE_DELAY_SECONDS = 60    # Delay between trading cycles

# === Logging ===
LOG_FILE = "trade_log.txt"
VERBOSE = False             # Enable detailed logging
