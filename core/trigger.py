# core/trigger.py

from config import trade_config as cfg

def confirm_trade(signal_data):
    """
    Confirms trade manually unless AUTO_MODE is enabled.
    """
    if cfg.AUTO_MODE:
        return True  # Auto mode skips confirmation

    print("\n📋 Trade Signal Detected:")
    print(f"Asset: {signal_data['asset']}")
    print(f"Action: {signal_data['action']}")
    print(f"Confidence: {signal_data['confidence']}")
    print(f"Timestamp: {signal_data['timestamp']}")
    
    user_input = input("👉 Confirm trade? (y/n): ").strip().lower()
    return user_input == 'y'
