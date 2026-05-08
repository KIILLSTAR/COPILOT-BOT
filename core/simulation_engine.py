"""
Dry Run Simulation Engine
Mimics live Jupiter perp trading with real market data.
No real money ever moves. Safety is hardcoded.
"""
from __future__ import annotations
import json, os, uuid
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict, field
from core.price_fetcher import price_fetcher

@dataclass
class SimPosition:
    id: str
    symbol: str
    side: str           # "long" or "short"
    entry_price: float
    size_usd: float
    leverage: float
    entry_time: str
    current_price: float = 0.0
    unrealized_pnl: float = 0.0
    realized_pnl: float = 0.0
    status: str = "open"
    exit_price: Optional[float] = None
    exit_time: Optional[str] = None
    stop_loss: Optional[float] = None
    take_profit: Optional[float] = None
    fees_paid: float = 0.0

@dataclass
class SimMetrics:
    total_trades: int = 0
    winning_trades: int = 0
    losing_trades: int = 0
    total_pnl: float = 0.0
    total_fees: float = 0.0
    win_rate: float = 0.0
    avg_win: float = 0.0
    avg_loss: float = 0.0
    largest_win: float = 0.0
    largest_loss: float = 0.0
    max_drawdown: float = 0.0
    starting_balance: float = 10_000.0
    current_balance: float = 10_000.0

class TradingSimulator:
    STATE_FILE = "data/simulation_state.json"

    def __init__(self, starting_balance: float = 10_000.0):
        self.starting_balance = starting_balance
        self.current_balance = starting_balance
        self.positions: Dict[str, SimPosition] = {}
        self.trade_history: List[SimPosition] = []
        self.metrics = SimMetrics(
            starting_balance=starting_balance,
            current_balance=starting_balance
        )
        os.makedirs("data", exist_ok=True)
        self._load_state()

    # ── State persistence ──────────────────────────────────────────────────

    def _load_state(self):
        if not os.path.exists(self.STATE_FILE):
            return
        try:
            with open(self.STATE_FILE) as f:
                d = json.load(f)
            self.current_balance = d.get("balance", self.starting_balance)
            self.metrics = SimMetrics(**d.get("metrics", asdict(self.metrics)))
            for pid, pos_dict in d.get("positions", {}).items():
                self.positions[pid] = SimPosition(**pos_dict)
            for pos_dict in d.get("history", []):
                self.trade_history.append(SimPosition(**pos_dict))
        except Exception as e:
            print(f"[Sim] Could not load state: {e}")

    def _save_state(self):
        try:
            with open(self.STATE_FILE, "w") as f:
                json.dump({
                    "balance": self.current_balance,
                    "metrics": asdict(self.metrics),
                    "positions": {pid: asdict(p) for pid, p in self.positions.items()},
                    "history": [asdict(p) for p in self.trade_history[-200:]]
                }, f, indent=2)
        except Exception as e:
            print(f"[Sim] Could not save state: {e}")

    # ── Position management ────────────────────────────────────────────────

    def open_position(self, side: str, size_usd: float, leverage: float,
                      symbol: str = "ETH-PERP",
                      stop_loss_pct: float = 0.02,
                      take_profit_pct: float = 0.04) -> SimPosition:
        price = price_fetcher.get_eth_price()
        fee = size_usd * leverage * 0.001  # 0.1% maker/taker
        self.current_balance -= fee

        sl = price * (1 - stop_loss_pct) if side == "long" else price * (1 + stop_loss_pct)
        tp = price * (1 + take_profit_pct) if side == "long" else price * (1 - take_profit_pct)

        pos = SimPosition(
            id=str(uuid.uuid4())[:8],
            symbol=symbol,
            side=side,
            entry_price=price,
            size_usd=size_usd,
            leverage=leverage,
            entry_time=datetime.now(timezone.utc).isoformat(),
            current_price=price,
            fees_paid=fee,
            stop_loss=sl,
            take_profit=tp,
        )
        self.positions[pos.id] = pos
        self._save_state()
        return pos

    def update_positions(self) -> List[SimPosition]:
        """Refresh all open positions with current market price."""
        price = price_fetcher.get_eth_price()
        closed = []
        for pid, pos in list(self.positions.items()):
            pos.current_price = price
            notional = pos.size_usd * pos.leverage
            price_change_pct = (price - pos.entry_price) / pos.entry_price
            pos.unrealized_pnl = notional * price_change_pct if pos.side == "long" else notional * -price_change_pct

            # Check stop loss / take profit
            hit_sl = (pos.side == "long" and price <= pos.stop_loss) or \
                     (pos.side == "short" and price >= pos.stop_loss)
            hit_tp = (pos.side == "long" and price >= pos.take_profit) or \
                     (pos.side == "short" and price <= pos.take_profit)

            if hit_sl or hit_tp:
                closed.append(self.close_position(pid, reason="TP" if hit_tp else "SL"))
        self._save_state()
        return closed

    def close_position(self, position_id: str, reason: str = "manual") -> Optional[SimPosition]:
        pos = self.positions.pop(position_id, None)
        if not pos:
            return None
        price = price_fetcher.get_eth_price()
        pos.exit_price = price
        pos.exit_time = datetime.now(timezone.utc).isoformat()
        pos.status = f"closed:{reason}"

        notional = pos.size_usd * pos.leverage
        price_change_pct = (price - pos.entry_price) / pos.entry_price
        pos.realized_pnl = notional * price_change_pct if pos.side == "long" else notional * -price_change_pct
        close_fee = notional * 0.001
        pos.fees_paid += close_fee
        pos.realized_pnl -= close_fee
        pos.unrealized_pnl = 0

        self.current_balance += pos.realized_pnl
        self._update_metrics(pos)
        self.trade_history.append(pos)
        self._save_state()
        return pos

    def _update_metrics(self, pos: SimPosition):
        m = self.metrics
        m.total_trades += 1
        m.total_pnl += pos.realized_pnl
        m.total_fees += pos.fees_paid
        m.current_balance = self.current_balance
        if pos.realized_pnl > 0:
            m.winning_trades += 1
            m.avg_win = (m.avg_win * (m.winning_trades - 1) + pos.realized_pnl) / m.winning_trades
            m.largest_win = max(m.largest_win, pos.realized_pnl)
        else:
            m.losing_trades += 1
            ct = m.losing_trades
            m.avg_loss = (m.avg_loss * (ct - 1) + pos.realized_pnl) / ct
            m.largest_loss = min(m.largest_loss, pos.realized_pnl)
        if m.total_trades > 0:
            m.win_rate = (m.winning_trades / m.total_trades) * 100
        peak = m.starting_balance
        trough = self.current_balance
        dd = (peak - trough) / peak * 100
        m.max_drawdown = max(m.max_drawdown, dd)

    def get_portfolio_summary(self) -> Dict[str, Any]:
        price = price_fetcher.get_eth_price()
        open_pnl = sum(p.unrealized_pnl for p in self.positions.values())
        return {
            "balance": round(self.current_balance, 2),
            "open_pnl": round(open_pnl, 2),
            "total_value": round(self.current_balance + open_pnl, 2),
            "total_pnl": round(self.metrics.total_pnl, 2),
            "total_trades": self.metrics.total_trades,
            "win_rate": round(self.metrics.win_rate, 1),
            "open_positions": len(self.positions),
            "eth_price": round(price, 2),
            "positions": [
                {
                    "id": p.id, "side": p.side, "entry": round(p.entry_price, 2),
                    "current": round(p.current_price, 2), "pnl": round(p.unrealized_pnl, 2),
                    "size_usd": p.size_usd, "leverage": p.leverage,
                    "sl": round(p.stop_loss, 2), "tp": round(p.take_profit, 2)
                }
                for p in self.positions.values()
            ],
            "recent_trades": [
                {
                    "id": p.id, "side": p.side, "entry": round(p.entry_price, 2),
                    "exit": round(p.exit_price, 2) if p.exit_price else None,
                    "pnl": round(p.realized_pnl, 2), "status": p.status,
                    "time": p.exit_time
                }
                for p in self.trade_history[-10:]
            ]
        }

# Singleton
simulator = TradingSimulator()
