from wallet.logger import log_info, log_event
log_info("Signal detected for SOL")

def select_best_signal(signals: dict) -> str:
    priority = {"breakout": 3, "dip": 2, "sideways": 1, "error": 0}
    sorted_signals = sorted(signals.items(), key=lambda x: priority.get(x[1], 0), reverse=True)
    return sorted_signals[0][0] if sorted_signals else None
