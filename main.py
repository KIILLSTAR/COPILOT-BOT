# main.py - Jupiter ETH Perps Trading Bot with Dry Run Simulation

from ai_signal_detector import run_ai_signal_loop
from app_core_trading import run_pnl_monitor
from app_config import trade_config as cfg
from app_logger import _write_log
import time
import threading

def main():
    print("🚀 Starting Jupiter ETH Perps Trading Bot")
    print(f"Mode: {'DRY-RUN' if cfg.DRY_RUN else 'LIVE'} | Auto: {cfg.AUTO_MODE}")
    
    # Initialize simulation engine
    from core.simulation_engine import simulator
    from app_dashboard import start_trading_dashboard
    
    _write_log("BOOT", "Bot initialized")
    
    # Ask user if they want the dashboard
    print("\n📊 Would you like to run the interactive dashboard? (y/N): ", end="")
    try:
        # For background agent, we'll default to showing status without interactive dashboard
        dashboard_choice = "n"
        print("n (Background mode)")
    except:
        dashboard_choice = "n"
    
    dashboard_thread = None
    if dashboard_choice.lower() == 'y':
        print("🚀 Starting dashboard in background...")
        dashboard_thread = start_trading_dashboard(interactive=False)
        time.sleep(2)  # Give dashboard time to start
    
    print(f"\n✅ Bot started successfully!")
    print(f"💰 Simulation Balance: ${simulator.current_balance:,.2f}")
    print(f"📈 Portfolio Value: ${simulator.get_portfolio_summary()['total_value']:,.2f}")
    
    if cfg.DRY_RUN:
        print("🧪 DRY RUN MODE: All trades will be simulated with real market data")
        print("   - Real-time ETH prices from multiple sources")
        print("   - Realistic fees, slippage, and funding costs")
        print("   - Complete trade history and performance analytics")
    else:
        print("🔴 LIVE TRADING MODE: Real money will be used!")
    
    print("\nPress Ctrl+C to stop the bot\n")

    try:
        cycle_count = 0
        while True:
            cycle_count += 1
            print(f"\n{'='*50}")
            print(f"📊 TRADING CYCLE #{cycle_count}")
            print(f"{'='*50}")
            
            # Update existing positions first
            if cfg.DRY_RUN:
                simulator.update_positions()
                
                # Show quick status
                portfolio = simulator.get_portfolio_summary()
                print(f"💰 Balance: ${portfolio['balance']:,.2f} | "
                      f"PnL: ${portfolio['total_pnl']:,.2f} | "
                      f"Open: {portfolio['open_positions']} positions")
            
            # 🔍 Detect and process signal
            print("\n🔍 Running signal detection...")
            signal_result = run_ai_signal_loop(cfg)
            
            # 📊 Monitor PnL after trade
            print("\n📊 Monitoring positions...")
            run_pnl_monitor(cfg)
            
            # Show simulation summary periodically
            if cfg.DRY_RUN and cycle_count % 5 == 0:  # Every 5 cycles
                portfolio = simulator.get_portfolio_summary()
                print(f"\n📈 SIMULATION SUMMARY (Cycle {cycle_count}):")
                print(f"   Total Trades: {portfolio['total_trades']}")
                print(f"   Win Rate: {portfolio['win_rate']:.1f}%")
                print(f"   ROI: {portfolio['roi']:.2f}%")
                print(f"   Unrealized PnL: ${portfolio['unrealized_pnl']:,.2f}")
            
            # ⏱️ Sleep between cycles
            cycle_delay = getattr(cfg, 'CYCLE_DELAY_SECONDS', 60)
            print(f"\n⏱️  Waiting {cycle_delay} seconds until next cycle...")
            time.sleep(cycle_delay)

    except KeyboardInterrupt:
        _write_log("SHUTDOWN", "Bot stopped by user")
        print("\n\n🛑 Bot stopped manually.")
        
        # Show final simulation results
        if cfg.DRY_RUN:
            portfolio = simulator.get_portfolio_summary()
            print(f"\n📊 FINAL SIMULATION RESULTS:")
            print(f"   Starting Balance: ${simulator.starting_balance:,.2f}")
            print(f"   Final Balance: ${portfolio['balance']:,.2f}")
            print(f"   Total PnL: ${portfolio['total_pnl']:,.2f}")
            print(f"   ROI: {portfolio['roi']:.2f}%")
            print(f"   Total Trades: {portfolio['total_trades']}")
            print(f"   Win Rate: {portfolio['win_rate']:.1f}%")
            print(f"   Largest Win: ${portfolio['largest_win']:,.2f}")
            print(f"   Largest Loss: ${portfolio['largest_loss']:,.2f}")
            print(f"   Total Fees Paid: ${portfolio['total_fees']:,.2f}")
            
    except Exception as e:
        _write_log("ERROR", f"Bot crashed: {str(e)}")
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        if dashboard_thread:
            print("🔄 Stopping dashboard...")

if __name__ == "__main__":
    main()
