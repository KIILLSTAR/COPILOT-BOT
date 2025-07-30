# config/trade_config.py

# === Mode Toggles ===
DRY_RUN = True         # True = simulate trades, False = live execution
AUTO_MODE = False      # True = auto-confirm trades, False = manual confirmation

# === Strategy Parameters ===
SIGNAL_THRESHOLD = 0.75  # Minimum confidence to trigger a signal

# === Logging ===
LOG_FILE = "trade_log.txt"
