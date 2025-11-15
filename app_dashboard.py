"""
Consolidated Dashboard Module
Combines all dashboard functionality from various modules
"""
import os
import time
import json
import threading
from datetime import datetime
from typing import Dict, Any, List

# =============================================================================
# MINIMAL DASHBOARD (from dashboard/minimal_dashboard.py)
# =============================================================================

class MinimalDashboard:
    """
    Clean, minimalistic trading dashboard
    """
    
    def __init__(self):
        self.auto_approve = False
        self.show_help = False
        self.show_transactions = False
        self.running = False
        
    def clear(self):
        """Clear screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def header(self):
        """Simple header with safety status"""
        from config import safety
        
        # Safety check first
        forced_dry_run = safety.is_dry_run_forced()
        
        if forced_dry_run:
            mode = "🔒 SAFE DRY RUN"
            safety_symbol = "🛡️"
        else:
            mode = "⚠️ LIVE TRADING"
            safety_symbol = "⚠️"
            
        auto = "AUTO" if self.auto_approve else "MANUAL"
        
        print("┌─────────────────────────────────────────────────────────────┐")
        print(f"│ {safety_symbol} ETH PERPS BOT │ {mode:<12} │ {auto:<7} │ {datetime.now().strftime('%H:%M:%S')} │")
        print("└─────────────────────────────────────────────────────────────┘")
        
        # Safety status line
        if forced_dry_run:
            print("  🔒 SAFETY ACTIVE - YOUR FUNDS ARE PROTECTED")
        else:
            print("  ⚠️ WARNING: LIVE TRADING ENABLED - REAL MONEY AT RISK")
        
        # Quick stats
        try:
            from core.simulation_engine import simulator
            portfolio = simulator.get_portfolio_summary()
            balance = portfolio['balance']
            pnl = portfolio['total_pnl']
            trades = portfolio['total_trades']
            
            pnl_color = "+" if pnl >= 0 else ""
            print(f"  Balance: ${balance:,.0f}  │  PnL: {pnl_color}${pnl:,.0f}  │  Trades: {trades}")
        except:
            print("  Balance: $0  │  PnL: $0  │  Trades: 0")
        print()
    
    def main_menu(self):
        """Simple main menu"""
        print("Commands:")
        print("  [s] Start/Stop bot")
        print("  [a] Toggle auto-approve")
        print("  [t] Show transactions")
        print("  [h] Help")
        print("  [x] Safety status")
        print("  [q] Quit")
        print()
    
    def help_menu(self):
        """Expandable help menu"""
        if not self.show_help:
            return
            
        print("┌─ HELP ─────────────────────────────────────────────┐")
        print("│                                                    │")
        print("│  s  - Start/stop the trading bot                  │")
        print("│  a  - Toggle between auto and manual approval     │")
        print("│  t  - Show/hide transaction history               │")
        print("│  h  - Show/hide this help menu                    │")
        print("│  x  - Show detailed safety status                 │")
        print("│  q  - Quit the application                        │")
        print("│                                                    │")
        print("│  Auto Mode: Bot trades automatically              │")
        print("│  Manual Mode: You approve each trade              │")
        print("│                                                    │")
        print("│  🔒 SAFETY: Multiple layers protect your funds    │")
        print("│                                                    │")
        print("└────────────────────────────────────────────────────┘")
        print()
    
    def transactions_menu(self):
        """Expandable transactions menu"""
        if not self.show_transactions:
            return
            
        try:
            from core.simulation_engine import simulator
            
            print("┌─ TRANSACTIONS ─────────────────────────────────────┐")
            
            # Open positions
            if simulator.positions:
                print("│  OPEN POSITIONS:                                   │")
                for i, (pos_id, pos) in enumerate(simulator.positions.items(), 1):
                    side_symbol = "↗" if pos.side == "long" else "↘"
                    pnl_symbol = "+" if pos.unrealized_pnl >= 0 else ""
                    print(f"│  {i}. {side_symbol} {pos.symbol} ${pos.entry_price:.0f} → ${pos.current_price:.0f} ({pnl_symbol}${pos.unrealized_pnl:.0f})  │")
            else:
                print("│  No open positions                                │")
            
            print("│                                                    │")
            
            # Recent trades
            recent_trades = simulator.trade_history[-5:] if simulator.trade_history else []
            if recent_trades:
                print("│  RECENT TRADES:                                    │")
                for i, trade in enumerate(recent_trades, 1):
                    side_symbol = "↗" if trade.side == "long" else "↘"
                    pnl_symbol = "+" if trade.realized_pnl >= 0 else ""
                    entry_time = datetime.fromisoformat(trade.entry_time.replace('Z', '+00:00')).strftime('%m/%d %H:%M')
                    print(f"│  {i}. {side_symbol} {trade.symbol} {entry_time} ({pnl_symbol}${trade.realized_pnl:.0f})      │")
            else:
                print("│  No completed trades yet                          │")
            
            print("│                                                    │")
            print("└────────────────────────────────────────────────────┘")
        except:
            print("┌─ TRANSACTIONS ─────────────────────────────────────┐")
            print("│  No data available                                │")
            print("└────────────────────────────────────────────────────┘")
        print()
    
    def status_line(self):
        """Simple status line"""
        try:
            from core.simulation_engine import simulator
            status = "Running..." if self.running else "Stopped"
            open_positions = len(simulator.positions)
            print(f"Status: {status}  │  Open Positions: {open_positions}")
        except:
            status = "Running..." if self.running else "Stopped"
            print(f"Status: {status}  │  Open Positions: 0")
        print()
    
    def show_safety_status(self):
        """Display detailed safety status"""
        from config import safety
        
        self.clear()
        safety.print_safety_status()
        
        print("How to enable live trading (NOT RECOMMENDED):")
        print("1. Edit config.py - set SAFETY_LOCK_ENABLED = False")
        print("2. Set environment: ENABLE_LIVE_TRADING=TRUE")
        print("3. Create file: .live_trading_confirmed")
        print("4. Set environment: WALLET_APPROVED_LIVE_TRADING=TRUE")
        print()
        print("⚠️  ALL 4 steps required - any missing step forces dry run")
        print("💚 RECOMMENDATION: Keep safety enabled for testing")
        print()
        input("Press Enter to continue...")
        
        return True
    
    def display(self):
        """Display the complete dashboard"""
        self.clear()
        self.header()
        self.main_menu()
        self.help_menu()
        self.transactions_menu() 
        self.status_line()
        
        if not self.running:
            print("Enter command: ", end="", flush=True)
    
    def handle_command(self, cmd: str) -> bool:
        """Handle user commands - returns False to quit"""
        cmd = cmd.lower().strip()
        
        if cmd == 'q':
            return False
        elif cmd == 'h':
            self.show_help = not self.show_help
        elif cmd == 't':
            self.show_transactions = not self.show_transactions
        elif cmd == 'x':
            self.show_safety_status()
            return True
        elif cmd == 'a':
            self.auto_approve = not self.auto_approve
            mode = "AUTO" if self.auto_approve else "MANUAL"
            print(f"\n✓ Switched to {mode} mode")
            time.sleep(1)
        elif cmd == 's':
            self.running = not self.running
            if self.running:
                print("\n✓ Bot started")
                return 'start_bot'
            else:
                print("\n✓ Bot stopped") 
                time.sleep(1)
        else:
            if cmd:  # Only show error for non-empty commands
                print(f"\nUnknown command: {cmd}")
                time.sleep(1)
        
        return True
    
    def confirm_trade(self, signal: str, confidence: float, trade_size: float) -> bool:
        """Simple trade confirmation dialog"""
        if self.auto_approve:
            return True
            
        self.clear()
        print("┌─ TRADE CONFIRMATION ───────────────────────────────┐")
        print("│                                                    │")
        print(f"│  Direction: {signal.upper():<10}                             │")
        print(f"│  Confidence: {confidence:.1f}/5.0                            │")
        print(f"│  Size: ${trade_size:.0f}                                     │")
        print("│                                                    │")
        print("│  [y] Execute trade                                 │")
        print("│  [n] Skip trade                                    │")
        print("│  [a] Auto-approve (switch to auto mode)           │")
        print("│                                                    │")
        print("└────────────────────────────────────────────────────┘")
        print()
        
        while True:
            choice = input("Execute trade? [y/n/a]: ").lower().strip()
            if choice == 'y':
                return True
            elif choice == 'n':
                return False
            elif choice == 'a':
                self.auto_approve = True
                print("✓ Switched to auto mode")
                return True
            else:
                print("Please enter y, n, or a")
    
    def run_interactive(self):
        """Run interactive dashboard"""
        print("🚀 Starting Minimal Trading Dashboard...")
        time.sleep(1)
        
        try:
            while True:
                self.display()
                
                if self.running:
                    # Bot is running - simulate bot cycle
                    time.sleep(2)
                    continue
                
                # Wait for user input
                try:
                    cmd = input()
                    result = self.handle_command(cmd)
                    
                    if result == False:
                        break
                    elif result == 'start_bot':
                        return 'start_bot'  # Signal to start the trading bot
                        
                except KeyboardInterrupt:
                    break
                    
        except Exception as e:
            print(f"Dashboard error: {e}")
        
        print("\n👋 Dashboard closed")
        return 'quit'

# =============================================================================
# TRADING DASHBOARD (from dashboard/trading_dashboard.py)
# =============================================================================

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
        try:
            from core.simulation_engine import simulator
            from config import DRY_RUN, AUTO_MODE
            
            # Get portfolio summary
            portfolio = simulator.get_portfolio_summary()
            
            # Get current ETH price
            eth_price = simulator.get_real_time_price("ETH")
            
            return {
                "mode": "DRY RUN" if DRY_RUN else "LIVE TRADING",
                "auto_mode": AUTO_MODE,
                "eth_price": eth_price,
                "portfolio": portfolio,
                "positions": list(simulator.positions.values()),
                "recent_trades": simulator.trade_history[-5:] if simulator.trade_history else []
            }
        except:
            return {
                "mode": "DRY RUN",
                "auto_mode": False,
                "eth_price": 3000.0,
                "portfolio": {"balance": 0, "total_pnl": 0, "total_trades": 0},
                "positions": [],
                "recent_trades": []
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
        print(f"Balance:        {self.format_currency(portfolio.get('balance', 0))}")
        print(f"Unrealized PnL: {self.format_currency(portfolio.get('unrealized_pnl', 0))}")
        print(f"Total PnL:      {self.format_currency(portfolio.get('total_pnl', 0))}")
        print(f"Total Value:    {self.format_currency(portfolio.get('total_value', 0))}")
        print(f"ROI:            {self.format_percentage(portfolio.get('roi', 0))}")
        print()
        
        print("📈 TRADING STATS")
        print("-" * 40)
        print(f"Total Trades:   {portfolio.get('total_trades', 0)}")
        print(f"Win Rate:       {self.format_percentage(portfolio.get('win_rate', 0))}")
        print(f"Open Positions: {portfolio.get('open_positions', 0)}")
        print(f"Largest Win:    {self.format_currency(portfolio.get('largest_win', 0))}")
        print(f"Largest Loss:   {self.format_currency(portfolio.get('largest_loss', 0))}")
        print(f"Total Fees:     {self.format_currency(portfolio.get('total_fees', 0))}")
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
    
    def force_test_trade(self):
        """Force a test trade for demonstration"""
        try:
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
        except:
            print("❌ Test trade failed - simulation engine not available")

# =============================================================================
# WEB DASHBOARD (from dashboard/web_dashboard.py)
# =============================================================================

class WebDashboard:
    """
    Web-based dashboard using Flask
    """
    
    def __init__(self):
        self.app = None
        self.setup_flask()
    
    def setup_flask(self):
        """Setup Flask application"""
        try:
            from flask import Flask, render_template
            from config import DRY_RUN, LOG_FILE
            
            self.app = Flask(__name__)
            
            @self.app.route("/")
            def index():
                # Read log file
                logs = []
                if os.path.exists(LOG_FILE):
                    with open(LOG_FILE, "r") as f:
                        logs = f.readlines()
                return render_template("index.html", logs=logs, dry_run=DRY_RUN)
            
            @self.app.route("/logs")
            def logs():
                # Read log file
                logs = []
                if os.path.exists(LOG_FILE):
                    with open(LOG_FILE, "r") as f:
                        logs = f.readlines()
                return render_template("logs.html", logs=logs)
            
        except ImportError:
            print("Flask not available - web dashboard disabled")
            self.app = None
    
    def run(self, debug=True, port=5000):
        """Run the web dashboard"""
        if self.app:
            self.app.run(debug=debug, port=port)
        else:
            print("Web dashboard not available - Flask not installed")

# =============================================================================
# GLOBAL INSTANCES AND FUNCTIONS
# =============================================================================

# Global dashboard instances
minimal_dashboard = MinimalDashboard()
trading_dashboard = TradingDashboard()
web_dashboard = WebDashboard()

def start_minimal_dashboard():
    """Start the minimal dashboard"""
    return minimal_dashboard.run_interactive()

def start_trading_dashboard(interactive=True):
    """Start the trading dashboard"""
    if interactive:
        trading_dashboard.run_interactive()
    else:
        return trading_dashboard.run_background()

def start_web_dashboard(debug=True, port=5000):
    """Start the web dashboard"""
    web_dashboard.run(debug=debug, port=port)

# Backward compatibility
dashboard = minimal_dashboard

# Export all classes and functions
__all__ = [
    'MinimalDashboard', 'TradingDashboard', 'WebDashboard',
    'minimal_dashboard', 'trading_dashboard', 'web_dashboard',
    'start_minimal_dashboard', 'start_trading_dashboard', 'start_web_dashboard',
    'dashboard'
]