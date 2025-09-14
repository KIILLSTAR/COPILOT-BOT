"""
Consolidated Logger Module
Combines all logging functionality from various modules
"""
import os
import logging
from datetime import datetime
from typing import Dict, Any

# =============================================================================
# CONFIGURATION
# =============================================================================

# Create logs directory if it doesn't exist
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

# Timestamped log file name
LOG_FILE = os.path.join(LOG_DIR, f"bot_{datetime.now().strftime('%Y-%m-%d')}.log")

# Configure main logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

# Get logger instance
logger = logging.getLogger("TradingBot")

# =============================================================================
# AUDIT LOGGER (from logger/audit_logger.py)
# =============================================================================

def _write_log(entry_type: str, details: str):
    """Write log entry with timestamp"""
    timestamp = datetime.utcnow().isoformat()
    log_entry = f"[{entry_type}] {timestamp} | {details}\n"

    # Only create directory if LOG_PATH has a directory component
    log_dir = os.path.dirname("trade_log.txt")
    if log_dir:
        os.makedirs(log_dir, exist_ok=True)
    with open("trade_log.txt", "a") as f:
        f.write(log_entry)

def log_signal(signal: str):
    """Log trading signal"""
    _write_log("SIGNAL", signal)

def log_simulation(details: str):
    """Log simulation details"""
    _write_log("SIMULATION", details)

def log_execution(details: str):
    """Log trade execution"""
    _write_log("EXECUTION", details)

def log_pnl_alert(pnl: float):
    """Log PnL alert"""
    _write_log("PNL_ALERT", {"pnl": pnl})

def log_auto_close(pnl: float):
    """Log auto close event"""
    _write_log("AUTO_CLOSE", {"pnl": pnl})

# =============================================================================
# TRANSFER LOGGER (from safe_wallet_manager/transfer_logger.py)
# =============================================================================

def log_transfer(wallet: str, recipient: str, amount: float, tx_id: str):
    """Log wallet transfer"""
    with open(f"{LOG_DIR}/transfer_log.txt", "a") as f:
        f.write(f"{wallet} → {recipient} | {amount:.6f} SOL | tx: {tx_id}\n")

# =============================================================================
# GENERAL LOGGER (from wallet/logger.py)
# =============================================================================

def log_info(message: str):
    """Log info message"""
    logger.info(message)

def log_warning(message: str):
    """Log warning message"""
    logger.warning(message)

def log_error(message: str):
    """Log error message"""
    logger.error(message)

def log_debug(message: str):
    """Log debug message"""
    logger.debug(message)

def log_event(event_type: str, data: Dict[str, Any]):
    """Log structured event"""
    logger.info(f"[{event_type}] {data}")

# =============================================================================
# TRADE LOGGER (from utils/logger.py)
# =============================================================================

def log_trade_action(action: str):
    """Log trade action"""
    log_info(f"Trade Action: {action}")

# =============================================================================
# BACKWARD COMPATIBILITY
# =============================================================================

# For backward compatibility with existing imports
audit_logger = type('AuditLogger', (), {
    '_write_log': _write_log,
    'log_signal': log_signal,
    'log_simulation': log_simulation,
    'log_execution': log_execution,
    'log_pnl_alert': log_pnl_alert,
    'log_auto_close': log_auto_close,
})()

transfer_logger = type('TransferLogger', (), {
    'log_transfer': log_transfer,
})()

# Export all functions for easy importing
__all__ = [
    'logger', 'log_info', 'log_warning', 'log_error', 'log_debug', 'log_event',
    '_write_log', 'log_signal', 'log_simulation', 'log_execution', 
    'log_pnl_alert', 'log_auto_close', 'log_transfer', 'log_trade_action',
    'audit_logger', 'transfer_logger'
]