#!/usr/bin/env python3
"""
Jupiter ETH Perps Trading Bot - Minimal Interface
Clean, simple trading bot with minimalistic dashboard
"""
import time
import threading
from strategy.signal_detector import run_signal_loop
from core.pnl_moniter import run_pnl_monitor
from config import trade_config as cfg
from logger.audit_logger import _write_log
from dashboard.minimal_dashboard import start_minimal_dashboard, dashboard

class MinimalTradingBot:
    """
    Simplified trading bot with clean interface
    """
    
    def __init__(self):
        self.running = False
        self.bot_thread = None
        
    def trading_loop(self):
        """Main trading loop - simple and clean"""
        from core.simulation_engine import simulator
        
        cycle = 0
        while self.running:
            try:
                cycle += 1
                
                # Update existing positions
                if cfg.DRY_RUN:
                    simulator.update_positions()
                
                # Run signal detection
                signal_result = run_signal_loop(cfg)
                
                # Monitor PnL
                run_pnl_monitor(cfg)
                
                # Short pause between cycles
                time.sleep(cfg.CYCLE_DELAY_SECONDS)
                
            except Exception as e:
                _write_log("ERROR", f"Trading loop error: {e}")
                print(f"Error in trading loop: {e}")
                time.sleep(10)  # Wait before retrying
    
    def start(self):
        """Start the trading bot"""
        if self.running:
            return
            
        self.running = True
        dashboard.running = True
        
        # Start trading loop in background
        self.bot_thread = threading.Thread(target=self.trading_loop, daemon=True)
        self.bot_thread.start()
        
        _write_log("START", "Trading bot started")
    
    def stop(self):
        """Stop the trading bot"""
        if not self.running:
            return
            
        self.running = False
        dashboard.running = False
        
        if self.bot_thread:
            self.bot_thread.join(timeout=5)
        
        _write_log("STOP", "Trading bot stopped")

def main():
    """Main function - keep it simple"""
    print("🚀 Jupiter ETH Perps Trading Bot")
    print("Minimal Interface Edition")
    print()
    
    # Initialize
    from core.simulation_engine import simulator
    bot = MinimalTradingBot()
    
    # Show initial status
    portfolio = simulator.get_portfolio_summary()
    print(f"💰 Starting Balance: ${portfolio['balance']:,.0f}")
    print(f"🧪 Mode: {'DRY RUN' if cfg.DRY_RUN else 'LIVE TRADING'}")
    print()
    
    try:
        while True:
            # Run dashboard
            result = start_minimal_dashboard()
            
            if result == 'start_bot':
                print("\n🤖 Starting trading bot...")
                bot.start()
                
                # Keep bot running until user stops it
                while bot.running:
                    time.sleep(1)
                    
            elif result == 'quit':
                break
                
    except KeyboardInterrupt:
        print("\n\n🛑 Interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
    finally:
        # Cleanup
        bot.stop()
        
        # Show final results
        if cfg.DRY_RUN:
            portfolio = simulator.get_portfolio_summary()
            print(f"\n📊 Final Results:")
            print(f"   Balance: ${portfolio['balance']:,.0f}")
            print(f"   PnL: ${portfolio['total_pnl']:,.0f}")
            print(f"   Trades: {portfolio['total_trades']}")
            if portfolio['total_trades'] > 0:
                print(f"   Win Rate: {portfolio['win_rate']:.1f}%")
        
        print("\n👋 Goodbye!")

if __name__ == "__main__":
    main()