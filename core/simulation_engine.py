"""
Trading Simulation Engine
Handles dry run mode with real-time data and realistic trade execution simulation
"""
import json
import time
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
import requests

@dataclass
class SimulatedPosition:
    id: str
    symbol: str
    side: str  # "long" or "short"
    entry_price: float
    size: float
    leverage: float
    entry_time: str
    current_price: float
    unrealized_pnl: float
    realized_pnl: float = 0.0
    status: str = "open"  # "open", "closed"
    exit_price: Optional[float] = None
    exit_time: Optional[str] = None
    stop_loss: Optional[float] = None
    take_profit: Optional[float] = None
    fees_paid: float = 0.0
    funding_paid: float = 0.0

@dataclass
class SimulationMetrics:
    total_trades: int = 0
    winning_trades: int = 0
    losing_trades: int = 0
    total_pnl: float = 0.0
    total_fees: float = 0.0
    total_funding: float = 0.0
    win_rate: float = 0.0
    avg_win: float = 0.0
    avg_loss: float = 0.0
    largest_win: float = 0.0
    largest_loss: float = 0.0
    sharpe_ratio: float = 0.0
    max_drawdown: float = 0.0
    starting_balance: float = 10000.0
    current_balance: float = 10000.0

class TradingSimulator:
    """
    Realistic trading simulation with real market data
    """
    
    def __init__(self, starting_balance: float = 10000.0):
        self.starting_balance = starting_balance
        self.current_balance = starting_balance
        self.positions: Dict[str, SimulatedPosition] = {}
        self.trade_history: List[SimulatedPosition] = []
        self.metrics = SimulationMetrics(starting_balance=starting_balance, current_balance=starting_balance)
        self.simulation_file = "simulation_data.json"
        self.load_simulation_state()
    
    def get_real_time_price(self, symbol: str = "ETH") -> float:
        """Get real-time price from multiple sources"""
        try:
            # Try CoinGecko first
            response = requests.get(
                "https://api.coingecko.com/api/v3/simple/price",
                params={"ids": "ethereum", "vs_currencies": "usd"},
                timeout=5
            )
            if response.status_code == 200:
                return float(response.json()["ethereum"]["usd"])
        except:
            pass
        
        try:
            # Fallback to Jupiter price feed
            response = requests.get(
                "https://price.jup.ag/v4/price",
                params={"ids": "7vfCXTUXx5WJV5JADk17DUJ4ksgau7utNKj4b963voxs"},  # ETH mint
                timeout=5
            )
            if response.status_code == 200:
                data = response.json()
                if "data" in data and "7vfCXTUXx5WJV5JADk17DUJ4ksgau7utNKj4b963voxs" in data["data"]:
                    return float(data["data"]["7vfCXTUXx5WJV5JADk17DUJ4ksgau7utNKj4b963voxs"]["price"])
        except:
            pass
        
        # Fallback price if APIs fail
        return 3000.0
    
    def calculate_position_size(self, trade_size_usd: float, leverage: float, price: float) -> float:
        """Calculate position size based on trade parameters"""
        notional_size = trade_size_usd * leverage
        return notional_size / price
    
    def calculate_fees(self, notional_value: float) -> float:
        """Calculate trading fees (0.1% typical for perps)"""
        return notional_value * 0.001
    
    def calculate_funding_rate(self) -> float:
        """Simulate funding rate (simplified)"""
        import random
        # Simulate funding rate between -0.1% to 0.1% per 8 hours
        return random.uniform(-0.001, 0.001)
    
    def open_position(self, symbol: str, side: str, trade_size_usd: float, 
                     leverage: float = 1.0, stop_loss_pct: float = 0.02, 
                     take_profit_pct: float = 0.04) -> Optional[str]:
        """
        Open a simulated position with real market data
        """
        current_price = self.get_real_time_price(symbol)
        position_size = self.calculate_position_size(trade_size_usd, leverage, current_price)
        notional_value = position_size * current_price
        fees = self.calculate_fees(notional_value)
        
        # Check if we have enough balance
        if fees > self.current_balance:
            print(f"❌ Insufficient balance for fees: ${fees:.2f}")
            return None
        
        # Create position
        position_id = f"{symbol}_{side}_{int(time.time())}"
        
        # Calculate stop loss and take profit
        if side == "long":
            stop_loss = current_price * (1 - stop_loss_pct)
            take_profit = current_price * (1 + take_profit_pct)
        else:  # short
            stop_loss = current_price * (1 + stop_loss_pct)
            take_profit = current_price * (1 - take_profit_pct)
        
        position = SimulatedPosition(
            id=position_id,
            symbol=symbol,
            side=side,
            entry_price=current_price,
            size=position_size,
            leverage=leverage,
            entry_time=datetime.now(timezone.utc).isoformat(),
            current_price=current_price,
            unrealized_pnl=0.0,
            stop_loss=stop_loss,
            take_profit=take_profit,
            fees_paid=fees
        )
        
        self.positions[position_id] = position
        self.current_balance -= fees
        self.metrics.total_fees += fees
        
        print(f"📈 Opened {side.upper()} position: {symbol}")
        print(f"   Entry: ${current_price:.2f} | Size: {position_size:.4f} {symbol}")
        print(f"   Stop Loss: ${stop_loss:.2f} | Take Profit: ${take_profit:.2f}")
        print(f"   Fees: ${fees:.2f} | Balance: ${self.current_balance:.2f}")
        
        self.save_simulation_state()
        return position_id
    
    def update_positions(self):
        """Update all open positions with current market data"""
        positions_to_close = []
        
        for position_id, position in self.positions.items():
            if position.status != "open":
                continue
            
            # Get current price
            current_price = self.get_real_time_price(position.symbol)
            position.current_price = current_price
            
            # Calculate unrealized PnL
            if position.side == "long":
                price_diff = current_price - position.entry_price
            else:  # short
                price_diff = position.entry_price - current_price
            
            position.unrealized_pnl = (price_diff / position.entry_price) * position.size * position.entry_price * position.leverage
            
            # Apply funding costs (simplified)
            funding_rate = self.calculate_funding_rate()
            funding_cost = position.size * current_price * funding_rate
            position.funding_paid += funding_cost
            
            # Check stop loss and take profit
            should_close = False
            close_reason = ""
            
            if position.side == "long":
                if current_price <= position.stop_loss:
                    should_close = True
                    close_reason = "Stop Loss"
                elif current_price >= position.take_profit:
                    should_close = True
                    close_reason = "Take Profit"
            else:  # short
                if current_price >= position.stop_loss:
                    should_close = True
                    close_reason = "Stop Loss"
                elif current_price <= position.take_profit:
                    should_close = True
                    close_reason = "Take Profit"
            
            if should_close:
                positions_to_close.append((position_id, close_reason))
        
        # Close positions that hit stop loss or take profit
        for position_id, reason in positions_to_close:
            self.close_position(position_id, reason)
    
    def close_position(self, position_id: str, reason: str = "Manual") -> bool:
        """Close a simulated position"""
        if position_id not in self.positions:
            return False
        
        position = self.positions[position_id]
        if position.status != "open":
            return False
        
        # Get current price for exit
        current_price = self.get_real_time_price(position.symbol)
        exit_fees = self.calculate_fees(position.size * current_price)
        
        # Calculate final PnL
        if position.side == "long":
            price_diff = current_price - position.entry_price
        else:  # short
            price_diff = position.entry_price - current_price
        
        realized_pnl = (price_diff / position.entry_price) * position.size * position.entry_price * position.leverage
        realized_pnl -= (position.fees_paid + exit_fees + position.funding_paid)
        
        # Update position
        position.status = "closed"
        position.exit_price = current_price
        position.exit_time = datetime.now(timezone.utc).isoformat()
        position.realized_pnl = realized_pnl
        position.fees_paid += exit_fees
        
        # Update balance and metrics
        self.current_balance += realized_pnl
        self.metrics.current_balance = self.current_balance
        self.metrics.total_pnl += realized_pnl
        self.metrics.total_fees += exit_fees
        self.metrics.total_funding += position.funding_paid
        self.metrics.total_trades += 1
        
        if realized_pnl > 0:
            self.metrics.winning_trades += 1
            if realized_pnl > self.metrics.largest_win:
                self.metrics.largest_win = realized_pnl
        else:
            self.metrics.losing_trades += 1
            if realized_pnl < self.metrics.largest_loss:
                self.metrics.largest_loss = realized_pnl
        
        # Move to trade history
        self.trade_history.append(position)
        del self.positions[position_id]
        
        # Update win rate
        if self.metrics.total_trades > 0:
            self.metrics.win_rate = self.metrics.winning_trades / self.metrics.total_trades
        
        print(f"🏁 Closed {position.side.upper()} position: {position.symbol}")
        print(f"   Entry: ${position.entry_price:.2f} → Exit: ${current_price:.2f}")
        print(f"   PnL: ${realized_pnl:.2f} | Reason: {reason}")
        print(f"   Balance: ${self.current_balance:.2f}")
        
        self.save_simulation_state()
        return True
    
    def get_portfolio_summary(self) -> Dict[str, Any]:
        """Get comprehensive portfolio summary"""
        # Update positions first
        self.update_positions()
        
        total_unrealized = sum(pos.unrealized_pnl for pos in self.positions.values())
        
        return {
            "balance": self.current_balance,
            "total_pnl": self.metrics.total_pnl,
            "unrealized_pnl": total_unrealized,
            "total_value": self.current_balance + total_unrealized,
            "open_positions": len(self.positions),
            "total_trades": self.metrics.total_trades,
            "win_rate": self.metrics.win_rate * 100,
            "largest_win": self.metrics.largest_win,
            "largest_loss": self.metrics.largest_loss,
            "total_fees": self.metrics.total_fees,
            "roi": ((self.current_balance - self.starting_balance) / self.starting_balance) * 100
        }
    
    def save_simulation_state(self):
        """Save simulation state to file"""
        state = {
            "starting_balance": self.starting_balance,
            "current_balance": self.current_balance,
            "positions": {pid: asdict(pos) for pid, pos in self.positions.items()},
            "trade_history": [asdict(trade) for trade in self.trade_history],
            "metrics": asdict(self.metrics)
        }
        
        try:
            with open(self.simulation_file, 'w') as f:
                json.dump(state, f, indent=2)
        except Exception as e:
            print(f"Error saving simulation state: {e}")
    
    def load_simulation_state(self):
        """Load simulation state from file"""
        try:
            with open(self.simulation_file, 'r') as f:
                state = json.load(f)
            
            self.starting_balance = state.get("starting_balance", 10000.0)
            self.current_balance = state.get("current_balance", 10000.0)
            
            # Load positions
            self.positions = {}
            for pid, pos_data in state.get("positions", {}).items():
                self.positions[pid] = SimulatedPosition(**pos_data)
            
            # Load trade history
            self.trade_history = []
            for trade_data in state.get("trade_history", []):
                self.trade_history.append(SimulatedPosition(**trade_data))
            
            # Load metrics
            if "metrics" in state:
                self.metrics = SimulationMetrics(**state["metrics"])
            
            print(f"📊 Loaded simulation state: {len(self.positions)} open positions, {len(self.trade_history)} completed trades")
            
        except FileNotFoundError:
            print("📊 Starting fresh simulation")
        except Exception as e:
            print(f"Error loading simulation state: {e}")

# Global simulator instance
simulator = TradingSimulator()