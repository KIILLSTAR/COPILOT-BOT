from logger.audit_logger import _write_log

def execute_trade(signal_data):
    """
    Simulated trade execution.
    Replace with real trade logic (e.g., Drift SDK call).
    """
    print(f"✅ Simulated Trade Executed: {signal_data['action']} {signal_data['asset']}")
    _write_log("EXECUTE", f"{signal_data['action']} {signal_data['asset']} @ {signal_data['timestamp']}")
