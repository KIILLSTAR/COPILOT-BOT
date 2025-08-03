"""
Interactive Trading Dashboard
Features dry run mode toggle and real-time simulation tracking
"""
import time
import json
from datetime import datetime
from typing import Dict, Any
import threading

# Simple console-based dashboard since we have limited dependencies
class TradingDashboard:
    """
    Console-based trading dashboard with dry run toggle
    """
    
    def __init__(self):
        self.is_running = False
        self.dry_run_mode = True
        self.refresh_rate = 5  # seconds
        self.last_update = None
        
    def clear_screen(self):
        """Clear the console screen"""
        import os
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def format_currency(self, amount: float) -> str:
        """Format currency with color coding"""
        if amount >= 0:
            return f"${amount:,.2f}"
        else:
            return f"-${abs(amount):,.2f}"
    
    def format_percentage(self, percentage: float) -> str:
        """Format percentage with color coding"""
        sign = "+" if percentage >= 0 else ""
        return f"{sign}{percentage:.2f}%"
    
    def get_bot_status(self) -> Dict[str, Any]:
        """Get current bot status and metrics"""
        from core.simulation_engine import simulator
        from config import trade_config as cfg
        
        # Get portfolio summary
        portfolio = simulator.get_portfolio_summary()
        
        # Get current ETH price
        eth_price = simulator.get_real_time_price("ETH")
        
        return {
            "mode": "DRY RUN" if cfg.DRY_RUN else "LIVE TRADING",
            "auto_mode": cfg.AUTO_MODE,
            "eth_price": eth_price,
            "portfolio": portfolio,
            "positions": list(simulator.positions.values()),
            "recent_trades": simulator.trade_history[-5:] if simulator.trade_history else []
        }
    
    def render_header(self, status: Dict[str, Any]):
        """Render dashboard header"""
        mode_indicator = "🧪 DRY RUN" if "DRY RUN" in status["mode"] else "🔴 LIVE"
        auto_indicator = "🤖 AUTO" if status["auto_mode"] else "👤 MANUAL"
        
        print("=" * 80)
        print(f"🚀 JUPITER ETH PERPS TRADING BOT {mode_indicator} {auto_indicator}")
        print("=" * 80)
        print(f"ETH Price: ${status['eth_price']:,.2f} | Last Update: {datetime.now().strftime('%H:%M:%S')}")
        print()
    
    def render_portfolio_summary(self, portfolio: Dict[str, Any]):
        """Render portfolio summary section"""
        print("📊 PORTFOLIO SUMMARY")
        print("-" * 40)
        print(f"Balance:        {self.format_currency(portfolio['balance'])}")
        print(f"Unrealized PnL: {self.format_currency(portfolio['unrealized_pnl'])}")
        print(f"Total PnL:      {self.format_currency(portfolio['total_pnl'])}")
        print(f"Total Value:    {self.format_currency(portfolio['total_value'])}")
        print(f"ROI:            {self.format_percentage(portfolio['roi'])}")
        print()
        
        print("📈 TRADING STATS")
        print("-" * 40)
        print(f"Total Trades:   {portfolio['total_trades']}")
        print(f"Win Rate:       {self.format_percentage(portfolio['win_rate'])}")
        print(f"Open Positions: {portfolio['open_positions']}")
        print(f"Largest Win:    {self.format_currency(portfolio['largest_win'])}")
        print(f"Largest Loss:   {self.format_currency(portfolio['largest_loss'])}")
        print(f"Total Fees:     {self.format_currency(portfolio['total_fees'])}")
        print()
    
    def render_open_positions(self, positions: list):
        """Render open positions"""
        if not positions:
            print("📋 OPEN POSITIONS: None")
            print()
            return
        
        print("📋 OPEN POSITIONS")
        print("-" * 80)
        print(f"{'Symbol':<8} {'Side':<6} {'Entry':<10} {'Current':<10} {'Size':<10} {'PnL':<12} {'%':<8}")
        print("-" * 80)
        
        for pos in positions:
            pnl_pct = (pos.unrealized_pnl / (pos.size * pos.entry_price)) * 100 if pos.size * pos.entry_price > 0 else 0
            print(f"{pos.symbol:<8} {pos.side.upper():<6} ${pos.entry_price:<9.2f} ${pos.current_price:<9.2f} "
                  f"{pos.size:<9.4f} {self.format_currency(pos.unrealized_pnl):<11} {self.format_percentage(pnl_pct):<8}")
        print()
    
    def render_recent_trades(self, trades: list):
        """Render recent completed trades"""
        if not trades:
            print("📝 RECENT TRADES: None")
            print()
            return
        
        print("📝 RECENT TRADES")
        print("-" * 80)
        print(f"{'Symbol':<8} {'Side':<6} {'Entry':<10} {'Exit':<10} {'PnL':<12} {'Time':<12}")
        print("-" * 80)
        
        for trade in trades:
            if trade.exit_time:
                exit_time = datetime.fromisoformat(trade.exit_time.replace('Z', '+00:00')).strftime('%H:%M:%S')
            else:
                exit_time = "N/A"
            
            print(f"{trade.symbol:<8} {trade.side.upper():<6} ${trade.entry_price:<9.2f} ${trade.exit_price or 0:<9.2f} "
                  f"{self.format_currency(trade.realized_pnl):<11} {exit_time:<12}")
        print()
    
    def render_controls(self):
        """Render control instructions"""
        print("🎮 CONTROLS")
        print("-" * 40)
        if self.dry_run_mode:
            print("Press 'L' + ENTER: Switch to LIVE trading")
        else:
            print("Press 'D' + ENTER: Switch to DRY RUN mode")
        print("Press 'Q' + ENTER: Quit dashboard")
        print("Press 'R' + ENTER: Reset simulation data")
        print("Press 'T' + ENTER: Force test trade")
        print()
    
    def toggle_dry_run_mode(self):
        """Toggle between dry run and live trading"""
        from config import trade_config as cfg
        
        if cfg.DRY_RUN:
            print("\n⚠️  SWITCHING TO LIVE TRADING MODE!")
            print("Are you sure? This will use real money! (y/N): ", end="")
            
            # In a real implementation, you'd get user input here
            # For now, we'll keep it in dry run for safety
            print("N (Safety override - staying in dry run)")
            return False
        else:
            cfg.DRY_RUN = True
            print("\n✅ Switched to DRY RUN mode")
            return True
    
    def reset_simulation(self):
        """Reset simulation data"""
        from core.simulation_engine import simulator
        
        print("\n⚠️  Reset simulation data? This will clear all trades and reset balance. (y/N): ", end="")
        # For demo purposes, we'll just show the message
        print("N (Demo mode - not resetting)")
        return False
    
    def force_test_trade(self):
        """Force a test trade for demonstration"""
        from core.simulation_engine import simulator
        import random
        
        # Create a random test trade
        side = random.choice(["long", "short"])
        trade_size = random.uniform(100, 500)
        
        print(f"\n🧪 Creating test {side} trade: ${trade_size:.2f}")
        position_id = simulator.open_position("ETH", side, trade_size, leverage=2.0)
        
        if position_id:
            print(f"✅ Test position created: {position_id}")
        else:
            print("❌ Failed to create test position")
    
    def display_dashboard(self):
        """Display the main dashboard"""
        try:
            # Get current status
            status = self.get_bot_status()
            
            # Clear screen and render dashboard
            self.clear_screen()
            
            # Render all sections
            self.render_header(status)
            self.render_portfolio_summary(status["portfolio"])
            self.render_open_positions(status["positions"])
            self.render_recent_trades(status["recent_trades"])
            self.render_controls()
            
            print(f"🔄 Auto-refresh every {self.refresh_rate}s | Last update: {datetime.now().strftime('%H:%M:%S')}")
            
        except Exception as e:
            print(f"❌ Dashboard error: {e}")
    
    def run_interactive(self):
        """Run interactive dashboard mode"""
        print("🚀 Starting Interactive Trading Dashboard...")
        print("Loading...")
        time.sleep(2)
        
        self.is_running = True
        
        try:
            while self.is_running:
                # Display dashboard
                self.display_dashboard()
                
                # Wait for refresh or user input
                print("\nEnter command (or wait for auto-refresh): ", end="", flush=True)
                
                # Simulate user input check (in real implementation, you'd use proper input handling)
                time.sleep(self.refresh_rate)
                
                # Simulate some commands for demo
                import random
                if random.random() < 0.1:  # 10% chance to simulate a test trade
                    self.force_test_trade()
                
        except KeyboardInterrupt:
            print("\n\n👋 Dashboard stopped by user")
        except Exception as e:
            print(f"\n❌ Dashboard error: {e}")
        finally:
            self.is_running = False
    
    def run_background(self):
        """Run dashboard in background mode (for bot integration)"""
        self.is_running = True
        
        def update_loop():
            while self.is_running:
                try:
                    # Just update the display without interaction
                    self.display_dashboard()
                    time.sleep(self.refresh_rate)
                except:
                    pass
        
        # Start background thread
        dashboard_thread = threading.Thread(target=update_loop, daemon=True)
        dashboard_thread.start()
        
        return dashboard_thread

# Dashboard instance
dashboard = TradingDashboard()

def start_dashboard(interactive=True):
    """Start the trading dashboard"""
    if interactive:
        dashboard.run_interactive()
    else:
        return dashboard.run_background()

if __name__ == "__main__":
    start_dashboard(interactive=True)