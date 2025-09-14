"""
Consolidated Trading Core Module
Combines small trading-related modules for better organization
"""
import random
from typing import Dict, Any, Optional

# =============================================================================
# TRADE EXECUTER (from core/excecuter.py)
# =============================================================================

def execute_trade(signal_data: Dict[str, Any]):
    """
    Simulated trade execution.
    Replace with real trade logic (e.g., Drift SDK call).
    """
    print(f"✅ Simulated Trade Executed: {signal_data['action']} {signal_data['asset']}")
    from logger import _write_log
    _write_log("EXECUTE", f"{signal_data['action']} {signal_data['asset']} @ {signal_data['timestamp']}")

# =============================================================================
# PNL MONITOR (from core/pnl_moniter.py)
# =============================================================================

def get_simulated_pnl() -> float:
    """
    Simulate a PnL value for testing.
    Replace with real Drift SDK call later.
    """
    return round(random.uniform(-25.0, 25.0), 2)

def check_pnl_thresholds():
    """Check PnL against configured thresholds"""
    from config import PNL_ALERT_THRESHOLD, MAX_LOSS_THRESHOLD, AUTO_CLOSE_ENABLED
    from logger import log_pnl_alert, log_auto_close
    
    pnl = get_simulated_pnl()
    print(f"[PnL Monitor] Simulated PnL: ${pnl}")

    if pnl >= PNL_ALERT_THRESHOLD:
        log_pnl_alert(pnl)
        print(f"[ALERT] Profit threshold hit: ${pnl}")

    if pnl <= -MAX_LOSS_THRESHOLD and AUTO_CLOSE_ENABLED:
        log_auto_close(pnl)
        print(f"[AUTO-CLOSE] Loss threshold hit: ${pnl}")

def run_pnl_monitor(cfg):
    """
    Call this periodically or after each trade.
    """
    check_pnl_thresholds()

# =============================================================================
# POSITION MANAGER (from core/position_manager.py)
# =============================================================================

def open_perp_position(drift_client, market_index: int, direction: str, size: float, leverage: float):
    """
    Open a perpetual position
    direction: "long" or "short"
    """
    drift_client.open_position(
        market_index=market_index,
        direction=direction,
        base_asset_amount=size,
        leverage=leverage
    )

def close_perp_position(drift_client, market_index: int):
    """Close a perpetual position"""
    drift_client.close_position(market_index)

# =============================================================================
# TRADE EXECUTER (from dashboard/dashboard.py - manual trade interface)
# =============================================================================

def manual_trade_interface():
    """
    Provides CLI or mobile-friendly manual control for Perp trades.
    """
    from config import AUTO_MODE, TRADE_SIZE_USD, DRY_RUN
    from logger import log_trade_action
    
    if not AUTO_MODE:
        print("Manual controls are disabled.")
        return

    try:
        from core.drift_client import init_drift_client
        from config import RPC_URL, KEYPAIR_PATH, MARKET_INDEX
        
        drift_client = init_drift_client(KEYPAIR_PATH, RPC_URL)
    except:
        print("Drift client not available - using simulation mode")
        drift_client = None

    while True:
        print("\n📱 Manual Trade Interface")
        print("1. Long ETH")
        print("2. Short ETH")
        print("3. Close Position")
        print("4. View Position Status")
        print("5. Exit")

        choice = input("Select an option: ").strip()

        if choice == "1":
            log_trade_action("Manual LONG selected.")
            if drift_client:
                execute_perp_trade("long", TRADE_SIZE_USD)
            else:
                print("✅ Simulated LONG trade executed")

        elif choice == "2":
            log_trade_action("Manual SHORT selected.")
            if drift_client:
                execute_perp_trade("short", TRADE_SIZE_USD)
            else:
                print("✅ Simulated SHORT trade executed")

        elif choice == "3":
            log_trade_action("Manual CLOSE selected.")
            if drift_client:
                execute_perp_trade("close", TRADE_SIZE_USD)
            else:
                print("✅ Simulated CLOSE trade executed")

        elif choice == "4":
            if drift_client:
                display_position_status(drift_client)
            else:
                print("🧪 Dry-run mode: No live position data.")

        elif choice == "5":
            print("Exiting manual interface.")
            break

        else:
            print("Invalid input. Try again.")

def display_position_status(drift_client):
    """
    Displays current ETH-PERP position status.
    """
    from config import DRY_RUN, MARKET_INDEX
    
    if DRY_RUN:
        print("🧪 Dry-run mode: No live position data.")
        return

    try:
        position = drift_client.get_user_position(market_index=MARKET_INDEX)

        if not position or position.base_asset_amount == 0:
            print("📭 No open position.")
            return

        direction = "LONG" if position.base_asset_amount > 0 else "SHORT"
        size = abs(position.base_asset_amount)
        entry_price = position.entry_price
        pnl = drift_client.get_unrealized_pnl(market_index=MARKET_INDEX)
        funding = drift_client.get_funding_rate(market_index=MARKET_INDEX)

        print(f"\n📊 Position Status:")
        print(f"Direction: {direction}")
        print(f"Size: {size} USD")
        print(f"Entry Price: {entry_price:.2f}")
        print(f"Unrealized PnL: {pnl:.2f} USD")
        print(f"Funding Rate: {funding:.4f}")

    except Exception as e:
        print(f"Error getting position status: {e}")

def execute_perp_trade(direction: str, size: float):
    """
    Execute a perpetual trade
    """
    try:
        from core.drift_client import init_drift_client
        from config import RPC_URL, KEYPAIR_PATH, MARKET_INDEX, LEVERAGE
        
        drift_client = init_drift_client(KEYPAIR_PATH, RPC_URL)
        
        if direction == "close":
            close_perp_position(drift_client, MARKET_INDEX)
        else:
            open_perp_position(drift_client, MARKET_INDEX, direction, size, LEVERAGE)
            
    except Exception as e:
        print(f"Trade execution error: {e}")

# =============================================================================
# EXPORTS
# =============================================================================

__all__ = [
    'execute_trade', 'get_simulated_pnl', 'check_pnl_thresholds', 'run_pnl_monitor',
    'open_perp_position', 'close_perp_position', 'manual_trade_interface',
    'display_position_status', 'execute_perp_trade'
]