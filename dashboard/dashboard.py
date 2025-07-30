# dashboard/dashboard.py

from trade_executor import execute_perp_trade
from config.trade_config import ENABLE_MANUAL_CONTROLS, TRADE_SIZE_USD, SHOW_POSITION_STATUS, DRY_RUN
from utils.logger import log_trade_action
from core.drift_client import init_drift_client
from config.trade_config import RPC_URL, KEYPAIR_PATH, MARKET_INDEX

def manual_trade_interface():
    """
    Provides CLI or mobile-friendly manual control for Perp trades.
    """
    if not ENABLE_MANUAL_CONTROLS:
        print("Manual controls are disabled.")
        return

    drift_client = init_drift_client(KEYPAIR_PATH, RPC_URL)

    while True:
        print("\n📱 Manual Trade Interface")
        print("1. Long ETH")
        print("2. Short ETH")
        print("3. Close Position")
        if SHOW_POSITION_STATUS:
            print("4. View Position Status")
            print("5. Exit")
        else:
            print("4. Exit")

        choice = input("Select an option: ").strip()

        if choice == "1":
            log_trade_action("Manual LONG selected.")
            execute_perp_trade("long", TRADE_SIZE_USD)

        elif choice == "2":
            log_trade_action("Manual SHORT selected.")
            execute_perp_trade("short", TRADE_SIZE_USD)

        elif choice == "3":
            log_trade_action("Manual CLOSE selected.")
            execute_perp_trade("close", TRADE_SIZE_USD)

        elif choice == "4" and SHOW_POSITION_STATUS:
            display_position_status(drift_client)

        elif choice == "5" or (choice == "4" and not SHOW_POSITION_STATUS):
            print("Exiting manual interface.")
            break

        else:
            print("Invalid input. Try again.")

def display_position_status(drift_client):
    """
    Displays current ETH-PERP position status.
    """
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

        log
