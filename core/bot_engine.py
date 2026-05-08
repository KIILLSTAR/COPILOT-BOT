"""
Main Bot Engine — orchestrates signal detection, simulation, and logging.
Single loop, clean and phone-friendly to monitor via the web dashboard.
"""
from __future__ import annotations
import time, json, os
from datetime import datetime, timezone
from typing import Optional
from config import trade_config as cfg
from config.safety_config import safety
from core.simulation_engine import simulator
from core.price_fetcher import price_fetcher
from strategy.signal_detector import detect_signal

LOG_FILE = cfg.LOG_FILE
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

def _log(level: str, msg: str):
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    line = f"[{ts}] [{level}] {msg}"
    print(line)
    try:
        with open(LOG_FILE, "a") as f:
            f.write(line + "\n")
    except Exception:
        pass

def run_cycle(cycle: int):
    _log("CYCLE", f"#{cycle} starting — DRY RUN: {cfg.DRY_RUN}")

    # 1. Update open positions (check SL/TP)
    closed = simulator.update_positions()
    for pos in closed:
        _log("CLOSE", f"Position {pos.id} closed | PnL: ${pos.realized_pnl:.2f} | Reason: {pos.status}")

    # 2. Detect signal
    signal = detect_signal(cfg)
    direction = signal["direction"]
    confidence = signal["confidence"]

    _log("SIGNAL", f"Direction={direction} | Confidence={confidence:.3f} | {signal['reason']}")

    # 3. Open position if signal is strong enough
    if direction != "none" and confidence >= cfg.SIGNAL_THRESHOLD:
        if cfg.AUTO_MODE or _manual_approve(signal):
            pos = simulator.open_position(
                side=direction,
                size_usd=cfg.TRADE_SIZE_USD,
                leverage=cfg.LEVERAGE,
                stop_loss_pct=cfg.STOP_LOSS_PCT,
                take_profit_pct=cfg.TAKE_PROFIT_PCT
            )
            _log("OPEN", f"{'[DRY RUN] ' if cfg.DRY_RUN else ''}Opened {direction.upper()} | "
                         f"Entry: ${pos.entry_price:.2f} | Size: ${pos.size_usd} | "
                         f"SL: ${pos.stop_loss:.2f} | TP: ${pos.take_profit:.2f}")

    # 4. Portfolio summary
    port = simulator.get_portfolio_summary()
    _log("STATUS", f"Balance: ${port['balance']:.2f} | Open PnL: ${port['open_pnl']:.2f} | "
                   f"Total PnL: ${port['total_pnl']:.2f} | Trades: {port['total_trades']} | "
                   f"Win Rate: {port['win_rate']}%")

def _manual_approve(signal: dict) -> bool:
    """In manual mode, auto-approve for background/web operation. Override via dashboard."""
    return True  # Dashboard will have approve/reject UI in next phase

def run_bot():
    _log("BOOT", f"COPILOT BOT starting — Mode: {'DRY RUN' if cfg.DRY_RUN else '⚠️ LIVE'} | "
                 f"Pair: {cfg.TRADING_PAIR} | Size: ${cfg.TRADE_SIZE_USD} | Leverage: {cfg.LEVERAGE}x")
    
    safety_status = safety.get_safety_status()
    _log("SAFETY", f"Dry run forced: {safety_status['forced_dry_run']} | "
                   f"Lock: {safety_status['safety_lock']}")

    cycle = 0
    while True:
        try:
            cycle += 1
            run_cycle(cycle)
        except KeyboardInterrupt:
            _log("STOP", "Bot stopped by user")
            break
        except Exception as e:
            _log("ERROR", f"Cycle {cycle} failed: {e}")
        time.sleep(cfg.CYCLE_DELAY_SECONDS)

if __name__ == "__main__":
    run_bot()
