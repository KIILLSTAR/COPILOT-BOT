# config/trade_config.py

import os

### 🚀 Trading Mode Toggles
DRY_RUN = True              # If True, simulate trades without executing
AUTO_MODE = True            # If True, strategy signals trigger trades automatically

### 🧠 Strategy Parameters
TRADE_SIZE_USD = 100        # Default trade size in USD
LEVERAGE = 5                # Leverage multiplier for Perp positions

### 📈 Drift Market Settings
MARKET_INDEX = 1            # ETH-PERP market index on Drift (confirm via SDK)
RPC_URL = "https://api.mainnet-beta.solana.com"  # Solana RPC endpoint

### 🔐 Wallet Settings
KEYPAIR_PATH = os.path.expanduser("~/.config/solana/id.json")  # Path to your wallet keypair

### 📊 Logging & Audit
LOG_PATH = "logs/trade_log.txt"  # Path to audit log file

### 📱 Dashboard Toggles
SHOW_POSITION_STATUS = True      # If True, dashboard shows open position info
ENABLE_MANUAL_CONTROLS = True    # If True, dashboard allows manual long/short/close

# PnL Monitoring
PNL_ALERT_THRESHOLD = 20.0       # USD profit to trigger alert
MAX_LOSS_THRESHOLD = 15.0        # USD loss to trigger auto-close
AUTO_CLOSE_ENABLED = True        # If True, auto-close on thresholds
