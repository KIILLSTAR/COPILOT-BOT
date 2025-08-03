# config/trade_config.py

# === Mode Toggles ===
DRY_RUN = True         # True = simulate trades, False = live execution
AUTO_MODE = False      # True = auto-confirm trades, False = manual confirmation

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
