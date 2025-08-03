"""
Minimalistic Trading Dashboard
Clean, simple interface with essential features only
"""
import os
import time
from datetime import datetime
from typing import Dict, Any, List

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
        """Simple header"""
        from config import trade_config as cfg
        from core.simulation_engine import simulator
        
        mode = "DRY RUN" if cfg.DRY_RUN else "LIVE"
        auto = "AUTO" if self.auto_approve else "MANUAL"
        
        print("┌─────────────────────────────────────────────────────────────┐")
        print(f"│  ETH PERPS BOT  │  {mode:<8}  │  {auto:<7}  │  {datetime.now().strftime('%H:%M:%S')}  │")
        print("└─────────────────────────────────────────────────────────────┘")
        
        # Quick stats
        portfolio = simulator.get_portfolio_summary()
        balance = portfolio['balance']
        pnl = portfolio['total_pnl']
        trades = portfolio['total_trades']
        
        pnl_color = "+" if pnl >= 0 else ""
        print(f"  Balance: ${balance:,.0f}  │  PnL: {pnl_color}${pnl:,.0f}  │  Trades: {trades}")
        print()
    
    def main_menu(self):
        """Simple main menu"""
        print("Commands:")
        print("  [s] Start/Stop bot")
        print("  [a] Toggle auto-approve")
        print("  [t] Show transactions")
        print("  [h] Help")
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
        print("│  q  - Quit the application                        │")
        print("│                                                    │")
        print("│  Auto Mode: Bot trades automatically              │")
        print("│  Manual Mode: You approve each trade              │")
        print("│                                                    │")
        print("└────────────────────────────────────────────────────┘")
        print()
    
    def transactions_menu(self):
        """Expandable transactions menu"""
        if not self.show_transactions:
            return
            
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
        print()
    
    def status_line(self):
        """Simple status line"""
        from core.simulation_engine import simulator
        
        status = "Running..." if self.running else "Stopped"
        open_positions = len(simulator.positions)
        
        print(f"Status: {status}  │  Open Positions: {open_positions}")
        print()
    
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

# Global dashboard instance
dashboard = MinimalDashboard()

def start_minimal_dashboard():
    """Start the minimal dashboard"""
    return dashboard.run_interactive()

if __name__ == "__main__":
    start_minimal_dashboard()