#!/usr/bin/env python3
"""
Demo: Minimal Trading Bot Interface
Shows the clean, simple dashboard in action
"""
import time
from core.simulation_engine import simulator
from dashboard.minimal_dashboard import dashboard

def create_sample_data():
    """Create some sample trading data for demonstration"""
    print("📊 Creating sample data...")
    
    # Create a few sample positions
    simulator.open_position("ETH", "long", 250, 1.5, 0.02, 0.04)
    time.sleep(1)
    simulator.open_position("ETH", "short", 180, 1.0, 0.025, 0.035)
    time.sleep(1)
    
    # Simulate some completed trades
    pos_id = simulator.open_position("ETH", "long", 100, 1.0, 0.02, 0.04)
    if pos_id:
        time.sleep(1)
        simulator.close_position(pos_id, "Demo - Take Profit")
    
    print("✅ Sample data created")

def demo_dashboard():
    """Demonstrate the minimal dashboard"""
    print("🚀 Minimal Dashboard Demo")
    print("=" * 30)
    print()
    print("Features:")
    print("  • Clean, simple interface")
    print("  • One-letter commands")
    print("  • Expandable help & transactions")
    print("  • Auto/manual trade approval")
    print("  • Real-time portfolio tracking")
    print()
    
    # Create sample data
    create_sample_data()
    
    print("🎮 Try these commands:")
    print("  h - Show/hide help")
    print("  t - Show/hide transactions")
    print("  a - Toggle auto-approve")
    print("  s - Start/stop bot")
    print("  q - Quit")
    print()
    input("Press Enter to start dashboard...")
    
    # Start the dashboard
    dashboard.run_interactive()

def demo_trade_approval():
    """Demonstrate trade approval process"""
    print("\n🤝 Trade Approval Demo")
    print("=" * 25)
    
    # Test manual approval
    dashboard.auto_approve = False
    approved = dashboard.confirm_trade("long", 3.2, 150)
    print(f"Manual approval result: {approved}")
    
    # Test auto approval
    dashboard.auto_approve = True
    approved = dashboard.confirm_trade("short", 2.8, 200)
    print(f"Auto approval result: {approved}")

if __name__ == "__main__":
    print("🧪 MINIMAL INTERFACE DEMO")
    print("=" * 40)
    
    try:
        demo_dashboard()
        
    except KeyboardInterrupt:
        print("\n\n👋 Demo ended")
    except Exception as e:
        print(f"\n❌ Demo error: {e}")