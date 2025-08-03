# main.py

from strategy.signal_detector import run_signal_loop
from core.pnl_moniter import run_pnl_monitor
from config import trade_config as cfg
from logger.audit_logger import _write_log
import time

def main():
    print("🚀 Starting Modular Trading Bot")
    print(f"Mode: {'DRY-RUN' if cfg.DRY_RUN else 'LIVE'} | Auto: {cfg.AUTO_MODE}")

    _write_log("BOOT", "Bot initialized")

    try:
        while True:
            # 🔍 Detect and process signal
            run_signal_loop(cfg)

            # 📊 Monitor PnL after trade
            run_pnl_monitor(cfg)

            # ⏱️ Sleep between cycles (adjust as needed)
            time.sleep(60)

    except KeyboardInterrupt:
        _write_log("SHUTDOWN", "Bot stopped by user")
        print("🛑 Bot stopped manually.")
    except Exception as e:
        _write_log("ERROR", f"Bot crashed: {str(e)}")
        print(f"[ERROR] {str(e)}")

if __name__ == "__main__":
    main()
