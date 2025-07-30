# core/signal_executor.py

from strategy.eth_strategy import generate_signal
from trade_executor import execute_perp_trade
from config.trade_config import AUTO_MODE, TRADE_SIZE_USD
from utils.logger import log_trade_action

def evaluate_and_execute():
    """
    Evaluates strategy signal and executes trade if AUTO_MODE is enabled.
    """
    signal = generate_signal()  # Expected: "long", "short", "close", or None

    if not signal:
        log_trade_action("No actionable signal. Holding.")
        return

    if AUTO_MODE:
        log_trade_action(f"AUTO_MODE active. Signal received: {signal}")
        execute_perp_trade(signal, TRADE_SIZE_USD)
    else:
        log_trade_action(f"AUTO_MODE off. Signal received: {signal}, awaiting manual confirmation.")
