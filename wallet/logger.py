# utils/logger.py

import logging
import os
from datetime import datetime

# ✅ Create logs directory if it doesn't exist
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

# ✅ Timestamped log file name
LOG_FILE = os.path.join(LOG_DIR, f"bot_{datetime.now().strftime('%Y-%m-%d')}.log")

# ✅ Configure logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

# ✅ Get logger instance
logger = logging.getLogger("TradingBot")

# ✅ Utility functions
def log_info(message: str):
    logger.info(message)

def log_warning(message: str):
    logger.warning(message)

def log_error(message: str):
    logger.error(message)

def log_debug(message: str):
    logger.debug(message)

# ✅ Optional: log structured events
def log_event(event_type: str, data: dict):
    logger.info(f"[{event_type}] {data}")
