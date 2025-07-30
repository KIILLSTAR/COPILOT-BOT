# dashboard/dashboard.py

from trade_executor import execute_perp_trade
from config.trade_config import ENABLE_MANUAL_CONTROLS, TRADE_SIZE_USD
from utils.logger import log_trade_action

def manual_trade_interface():
    """
    Provides CLI or mobile-friendly manual control for Perp trades.
    """
    if not ENABLE_MANUAL_CONTROLS:
        print("Manual controls are disabled.")
        return

    print("\n📱 Manual Trade Interface")
    print("1. Long ETH")
    print("2. Short ETH")
    print("3. Close Position")
    print("4. Exit")

    while True:
        choice = input("Select an option (1-4): ").strip()

        if choice == "1":
            log_trade_action("Manual LONG selected.")
            execute_perp_trade("long", TRADE_SIZE_USD)

        elif choice == "2":
            log_trade_action("Manual SHORT selected.")
            execute_perp_trade("short", TRADE_SIZE_USD)

        elif choice == "3":
            log_trade_action("Manual CLOSE selected.")
            execute_perp_trade("close", TRADE_SIZE_USD)

        elif choice == "4":
            print("Exiting manual interface.")
            break

        else:
            print("Invalid input. Try again.")
