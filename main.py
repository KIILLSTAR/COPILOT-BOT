# main.py

from core.signal_executor import evaluate_and_execute
from dashboard.dashboard import manual_trade_interface
from config.trade_config import AUTO_MODE, ENABLE_MANUAL_CONTROLS, DRY_RUN
from utils.logger import log_trade_action
import time

def run_bot():
    log_trade_action("🚀 ETH Perpetual Bot Started")
    log_trade_action(f"Mode: {'AUTO' if AUTO_MODE else 'MANUAL'}, Dry-run: {DRY_RUN}")

    try:
        while True:
            if AUTO_MODE:
                evaluate_and_execute()

            if ENABLE_MANUAL_CONTROLS:
                manual_trade_interface()

            # Sleep between cycles (adjust as needed)
            time.sleep(60)

    except KeyboardInterrupt:
        log_trade_action("🛑 Bot stopped by user.")
    except Exception as e:
        log_trade_action(f"[ERROR] Bot crashed: {str(e)}")

if __name__ == "__main__":
    run_bot()
