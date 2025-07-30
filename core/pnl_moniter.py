# core/pnl_monitor.py

import random
from config import trade_config as cfg
from logger.audit_logger import log_pnl_alert, log_auto_close

def get_simulated_pnl():
    """
    Simulate a PnL value for testing.
    Replace with real Drift SDK call later.
    """
    return round(random.uniform(-25.0, 25.0), 2)

def check_pnl_thresholds():
    pnl = get_simulated_pnl()
    print(f"[PnL Monitor] Simulated PnL: ${pnl}")

    if pnl >= cfg.PNL_ALERT_THRESHOLD:
        log_pnl_alert(pnl)
        print(f"[ALERT] Profit threshold hit: ${pnl}")

    if pnl <= -cfg.MAX_LOSS_THRESHOLD and cfg.AUTO_CLOSE_ENABLED:
        log_auto_close(pnl)
        print(f"[AUTO-CLOSE] Loss threshold hit: ${pnl}")

def run_pnl_monitor():
    """
    Call this periodically or after each trade.
    """
    check_pnl_thresholds()
