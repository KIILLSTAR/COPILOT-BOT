#!/usr/bin/env python3
"""
Main Trading Bot with Integrated Seamless AI Assistant
AI recommendations appear automatically during trading cycles
No need to run separate scripts - everything in one place
"""
from ai_signal_detector import run_ai_signal_loop
from app_core_trading import run_pnl_monitor
from app_config import trade_config as cfg
from app_logger import _write_log
from seamless_trading_assistant import SeamlessTradingAssistant
import time
import threading
import os

def main():
    print("🚀 Starting Jupiter ETH Perps Trading Bot with AI Assistant")
    print(f"Mode: {'DRY-RUN' if cfg.DRY_RUN else 'LIVE'} | Auto: {cfg.AUTO_MODE}")
    
    # Initialize simulation engine
    from core.simulation_engine import simulator
    from app_dashboard import start_trading_dashboard
    
    _write_log("BOOT", "Bot initialized")
    
    # Initialize AI Assistant (runs in background)
    print("\n🤖 Initializing AI Assistant...")
    ollama_url = os.getenv('OLLAMA_URL') or os.getenv('OLLAMA_CLOUD_URL')
    model_name = os.getenv('OLLAMA_MODEL', 'llama3.2')
    
    ai_assistant = None
    try:
        ai_assistant = SeamlessTradingAssistant(
            ollama_url=ollama_url,
            model_name=model_name,
            auto_refresh=0  # Manual refresh during trading cycles
        )
        
        # Test connection
        if ai_assistant.assistant.ollama.test_connection():
            print("✅ AI Assistant connected (Ollama cloud)")
        else:
            print("⚠️ AI Assistant unavailable - continuing without AI recommendations")
            ai_assistant = None
    except Exception as e:
        print(f"⚠️ Could not initialize AI Assistant: {e}")
        print("💡 Continuing without AI recommendations")
        ai_assistant = None
    
    # Ask user if they want the dashboard
    print("\n📊 Would you like to run the interactive dashboard? (y/N): ", end="")
    try:
        dashboard_choice = "n"
        print("n (Background mode)")
    except:
        dashboard_choice = "n"
    
    dashboard_thread = None
    if dashboard_choice.lower() == 'y':
        print("🚀 Starting dashboard in background...")
        dashboard_thread = start_trading_dashboard(interactive=False)
        time.sleep(2)
    
    print(f"\n✅ Bot started successfully!")
    print(f"💰 Simulation Balance: ${simulator.current_balance:,.2f}")
    print(f"📈 Portfolio Value: ${simulator.get_portfolio_summary()['total_value']:,.2f}")
    
    if ai_assistant:
        print("🤖 AI Assistant: Ready to provide recommendations during trading")
    
    if cfg.DRY_RUN:
        print("🧪 DRY RUN MODE: All trades will be simulated with real market data")
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
            
            # 🤖 Get AI recommendation BEFORE your signal detection
            if ai_assistant:
                print("\n🤖 Getting AI recommendation...")
                try:
                    ai_result = ai_assistant.analyze_and_recommend(show_details=False)
                    rec = ai_result['recommendation']
                    
                    print(f"\n{'='*50}")
                    print("🤖 AI RECOMMENDATION")
                    print(f"{'='*50}")
                    print(f"Action: {rec['action']} | Confidence: {rec['confidence']}/10")
                    
                    # Show key Jupiter data
                    if 'jupiter_insights' in ai_result:
                        jup = ai_result['jupiter_insights']
                        print(f"Jupiter Price: ${jup.get('eth_price', 0):,.2f} | "
                              f"Sentiment: {jup.get('sentiment', 'neutral').upper()}")
                    
                    # Show brief reasoning
                    analysis = ai_result.get('analysis', '')
                    if analysis:
                        brief_reason = analysis[:200] + "..." if len(analysis) > 200 else analysis
                        print(f"Reasoning: {brief_reason}")
                    
                    print(f"{'='*50}\n")
                    
                    # Log recommendation
                    _write_log("AI_ASSISTANT", 
                              f"Recommendation: {rec['action']} (Confidence: {rec['confidence']}/10)")
                    
                except Exception as e:
                    print(f"⚠️ AI recommendation unavailable: {e}")
            
            # 🔍 Detect and process signal (your existing logic)
            print("\n🔍 Running signal detection...")
            signal_result = run_ai_signal_loop(cfg)
            
            # 📊 Monitor PnL after trade
            print("\n📊 Monitoring positions...")
            run_pnl_monitor(cfg)
            
            # Show simulation summary periodically
            if cfg.DRY_RUN and cycle_count % 5 == 0:
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

