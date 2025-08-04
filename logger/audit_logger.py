# logger/audit_logger.py

import os
from config import trade_config as cfg
from datetime import datetime

LOG_PATH = cfg.LOG_FILE

def _write_log(entry_type, details):
    timestamp = datetime.utcnow().isoformat()
    log_entry = f"[{entry_type}] {timestamp} | {details}\n"

    # Only create directory if LOG_PATH has a directory component
    log_dir = os.path.dirname(LOG_PATH)
    if log_dir:
        os.makedirs(log_dir, exist_ok=True)
    with open(LOG_PATH, "a") as f:
        f.write(log_entry)

def log_signal(signal):
    _write_log("SIGNAL", signal)

def log_simulation(details):
    _write_log("SIMULATION", details)

def log_execution(details):
    _write_log("EXECUTION", details)

def log_pnl_alert(pnl):
    _write_log("PNL_ALERT", {"pnl": pnl})

def log_auto_close(pnl):
    _write_log("AUTO_CLOSE", {"pnl": pnl})
