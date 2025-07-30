# wallet/wallet_manager.py

from config import trade_config as cfg
from logger.audit_logger import log_simulation, log_execution

def simulate_trade(signal):
    """
    Simulate a trade without sending a transaction.
    Logs the action for audit purposes.
    """
    details = {
        "action": signal["action"],
        "token": signal["token"],
        "size": cfg.TRADE_SIZE_USD,
        "leverage": cfg.LEVERAGE,
        "status": "SIMULATED"
    }
    log_simulation(details)
    print(f"[SIMULATED] {details}")

def execute_trade(signal):
    """
    Placeholder for real trade execution.
    Replace with Drift SDK or transaction logic.
    """
    details = {
        "action": signal["action"],
        "token": signal["token"],
        "size": cfg.TRADE_SIZE_USD,
        "leverage": cfg.LEVERAGE,
        "status": "EXECUTED"
    }
    log_execution(details)
    print(f"[EXECUTED] {details}")
