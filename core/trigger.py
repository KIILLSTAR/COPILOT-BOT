# core/trigger.py

from config import trade_config as cfg

def confirm_trade(signal_data):
    if cfg.AUTO_MODE:
        return True  # Auto mode skips confirmation

    print(f"\n📋 Trade Signal Detected:\n{signal_data}")
    user_input = input("👉 Confirm trade? (y/n): ").strip().lower()
    return user_input == 'y'
