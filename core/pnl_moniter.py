# core/pnl_monitor.py

from core.drift_client import init_drift_client
from config.trade_config import (
    MARKET_INDEX,
    PNL_ALERT_THRESHOLD,
    AUTO_CLOSE_ENABLED,
    MAX_LOSS_THRESHOLD,
    DRY_RUN
)
from trade_executor import execute_perp_trade
from utils.logger import log_trade_action

def check_pnl_and_act():
    """
    Checks unrealized PnL and triggers alerts or auto-close if thresholds are hit.
    """
    if DRY_RUN:
        log_trade_action("🧪 Dry-run mode: Skipping PnL check.")
        return

    try:
        drift_client = init_drift_client()
        pnl = drift_client.get_unrealized_pnl(market_index=MARKET_INDEX)

        log_trade_action(f"📈 Current PnL: {pnl:.2f} USD")

        if pnl >= PNL_ALERT_THRESHOLD:
            log_trade_action(f"✅ PnL exceeds alert threshold: {pnl:.2f} USD")

            if AUTO_CLOSE_ENABLED:
                log_trade_action("Auto-close triggered due to profit target.")
                execute_perp_trade("close", size=0)

        elif pnl <= -MAX_LOSS_THRESHOLD:
            log_trade_action(f"⚠️ PnL below max loss threshold: {pnl:.2f} USD")

            if AUTO_CLOSE_ENABLED:
                log_trade_action("Auto-close triggered due to loss limit.")
                execute_perp_trade("close", size=0)

    except Exception as e:
        log_trade_action(f"[ERROR] PnL monitor failed: {str(e)}")
