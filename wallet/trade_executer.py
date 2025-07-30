# trade_executor.py

from core.drift_client import init_drift_client
from core.position_manager import open_perp_position, close_perp_position
from config.trade_config import (
    DRY_RUN,
    RPC_URL,
    KEYPAIR_PATH,
    MARKET_INDEX,
    LEVERAGE
)
from utils.logger import log_trade_action

# Initialize Drift client once
drift_client = init_drift_client(KEYPAIR_PATH, RPC_URL)

def execute_perp_trade(signal: str, size: float):
    """
    Executes a perpetual trade on Drift based on signal.
    signal: "long", "short", or "close"
    size: USD amount to trade
    """
    if DRY_RUN:
        log_trade_action(f"[DRY RUN] Signal: {signal}, Size: {size}, Leverage: {LEVERAGE}")
        return

    try:
        if signal == "long":
            log_trade_action(f"Executing LONG position: Size={size}, Leverage={LEVERAGE}")
            open_perp_position(drift_client, MARKET_INDEX, "long", size, LEVERAGE)

        elif signal == "short":
            log_trade_action(f"Executing SHORT position: Size={size}, Leverage={LEVERAGE}")
            open_perp_position(drift_client, MARKET_INDEX, "short", size, LEVERAGE)

        elif signal == "close":
            log_trade_action(f"Closing position on market index {MARKET_INDEX}")
            close_perp_position(drift_client, MARKET_INDEX)

        else:
            log_trade_action(f"Invalid signal received: {signal}")

    except Exception as e:
        log_trade_action(f"[ERROR] Trade execution failed: {str(e)}")
