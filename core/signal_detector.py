# strategy/signal_detector.py

import json
from config import trade_config as cfg
from wallet.wallet_manager import simulate_trade, execute_trade
from logger.audit_logger import log_signal

PENDING_SIGNAL_PATH = "logs/pending_signal.json"

def detect_signal():
    """
    Dummy signal generator for testing.
    Replace with real RSI/EMA/volume logic.
    """
    return {
        "token": "ETH-PERP",
        "action": "LONG",
        "confidence": 0.85
    }

def save_pending_signal(signal):
    with open(PENDING_SIGNAL_PATH, "w") as f:
        json.dump(signal, f)

def process_signal(signal):
    log_signal(signal)

    if cfg.DRY_RUN:
        simulate_trade(signal)
    elif cfg.AUTO_MODE:
        execute_trade(signal)
    else:
        save_pending_signal(signal)
        print("Signal saved for manual confirmation.")

def run_signal_loop():
    signal = detect_signal()
    if signal:
        process_signal(signal)
