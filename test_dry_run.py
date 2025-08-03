#!/usr/bin/env python3
"""
Test Script for Dry Run Simulation
Demonstrates the trading bot's simulation capabilities with real market data
"""
import time
import sys
from core.simulation_engine import simulator
from dashboard.trading_dashboard import dashboard

def test_simulation():
    """Test the simulation engine with sample trades"""
    print("🧪 TESTING DRY RUN SIMULATION")
    print("=" * 50)
    
    # Show initial state
    initial_portfolio = simulator.get_portfolio_summary()
    print(f"💰 Starting Balance: ${initial_portfolio['balance']:,.2f}")
    print(f"📊 Starting Portfolio Value: ${initial_portfolio['total_value']:,.2f}")
    
    # Get current ETH price
    eth_price = simulator.get_real_time_price("ETH")
    print(f"📈 Current ETH Price: ${eth_price:,.2f}")
    
    print("\n🔄 Creating test positions...")
    
    # Test Position 1: Long ETH
    print("\n📈 Opening LONG position...")
    long_position = simulator.open_position(
        symbol="ETH",
        side="long", 
        trade_size_usd=500,
        leverage=2.0,
        stop_loss_pct=0.03,  # 3% stop loss
        take_profit_pct=0.05  # 5% take profit
    )
    
    if long_position:
        print(f"✅ Long position created: {long_position}")
    
    time.sleep(2)
    
    # Test Position 2: Short ETH
    print("\n📉 Opening SHORT position...")
    short_position = simulator.open_position(
        symbol="ETH",
        side="short",
        trade_size_usd=300,
        leverage=1.5,
        stop_loss_pct=0.025,  # 2.5% stop loss
        take_profit_pct=0.04   # 4% take profit
    )
    
    if short_position:
        print(f"✅ Short position created: {short_position}")
    
    time.sleep(2)
    
    # Show current portfolio state
    print("\n📊 PORTFOLIO STATUS AFTER OPENING POSITIONS:")
    portfolio = simulator.get_portfolio_summary()
    for key, value in portfolio.items():
        if isinstance(value, float):
            print(f"   {key.replace('_', ' ').title()}: ${value:,.2f}")
        else:
            print(f"   {key.replace('_', ' ').title()}: {value}")
    
    # Monitor positions for a few cycles
    print("\n🔄 Monitoring positions...")
    for cycle in range(3):
        print(f"\n--- Monitoring Cycle {cycle + 1} ---")
        simulator.update_positions()
        
        # Show position details
        for pos_id, position in simulator.positions.items():
            print(f"Position {pos_id[:8]}...")
            print(f"  {position.side.upper()} {position.symbol}")
            print(f"  Entry: ${position.entry_price:.2f} → Current: ${position.current_price:.2f}")
            print(f"  Unrealized PnL: ${position.unrealized_pnl:.2f}")
            
        time.sleep(5)  # Wait 5 seconds between updates
    
    # Manually close one position
    if simulator.positions:
        position_to_close = list(simulator.positions.keys())[0]
        print(f"\n🏁 Manually closing position: {position_to_close[:8]}...")
        success = simulator.close_position(position_to_close, "Manual Test Close")
        if success:
            print("✅ Position closed successfully")
    
    # Final portfolio summary
    print("\n📊 FINAL PORTFOLIO SUMMARY:")
    final_portfolio = simulator.get_portfolio_summary()
    for key, value in final_portfolio.items():
        if isinstance(value, float):
            print(f"   {key.replace('_', ' ').title()}: ${value:,.2f}")
        else:
            print(f"   {key.replace('_', ' ').title()}: {value}")
    
    # Show trade history
    if simulator.trade_history:
        print(f"\n📝 COMPLETED TRADES ({len(simulator.trade_history)}):")
        for trade in simulator.trade_history[-3:]:  # Show last 3 trades
            print(f"   {trade.symbol} {trade.side.upper()}: "
                  f"${trade.entry_price:.2f} → ${trade.exit_price:.2f} = "
                  f"${trade.realized_pnl:.2f}")

def test_dashboard():
    """Test the dashboard display"""
    print("\n📊 TESTING DASHBOARD DISPLAY")
    print("=" * 50)
    
    # Display dashboard once
    dashboard.display_dashboard()

def main():
    """Main test function"""
    print("🚀 Jupiter ETH Perps Trading Bot - Dry Run Test")
    print("This test demonstrates the simulation capabilities\n")
    
    try:
        # Test simulation engine
        test_simulation()
        
        print("\n" + "=" * 50)
        input("Press Enter to test dashboard display...")
        
        # Test dashboard
        test_dashboard()
        
        print("\n✅ All tests completed successfully!")
        print("\n💡 To run the full bot with continuous simulation:")
        print("   python3 main.py")
        
    except KeyboardInterrupt:
        print("\n\n🛑 Test interrupted by user")
    except Exception as e:
        print(f"\n❌ Test error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()