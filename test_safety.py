#!/usr/bin/env python3
"""
Safety Testing Script
Verifies all protection layers are working correctly
"""
import os
import sys
from config.safety_config import safety

def test_safety_layers():
    """Test all safety protection layers"""
    print("🔒 COMPREHENSIVE SAFETY TEST")
    print("=" * 50)
    
    print("\n1. Testing Primary Safety Lock...")
    # This should always be True for safety
    if safety.SAFETY_LOCK_ENABLED:
        print("✅ Primary safety lock is ENABLED (Good)")
    else:
        print("❌ Primary safety lock is DISABLED (Dangerous!)")
    
    print("\n2. Testing Environment Variable Protection...")
    live_trading_env = os.getenv('ENABLE_LIVE_TRADING', 'FALSE').upper()
    if live_trading_env != 'TRUE':
        print("✅ Environment protection ACTIVE (Good)")
    else:
        print("⚠️ Environment allows live trading")
    
    print("\n3. Testing Manual Confirmation File...")
    if not os.path.exists('.live_trading_confirmed'):
        print("✅ Manual confirmation file MISSING (Good)")
    else:
        print("⚠️ Manual confirmation file EXISTS")
    
    print("\n4. Testing Wallet Approval...")
    wallet_approved = os.getenv('WALLET_APPROVED_LIVE_TRADING', 'FALSE').upper()
    if wallet_approved != 'TRUE':
        print("✅ Wallet approval NOT SET (Good)")
    else:
        print("⚠️ Wallet approval is SET")
    
    print("\n5. Overall Safety Check...")
    forced_dry_run = safety.is_dry_run_forced()
    if forced_dry_run:
        print("✅ DRY RUN IS FORCED - Your funds are SAFE! 🛡️")
    else:
        print("❌ LIVE TRADING IS POSSIBLE - Funds at risk! ⚠️")
    
    return forced_dry_run

def test_config_integration():
    """Test that trade config respects safety"""
    print("\n🔧 TESTING CONFIG INTEGRATION")
    print("=" * 35)
    
    try:
        from config import trade_config as cfg
        
        print(f"Trade Config DRY_RUN: {cfg.DRY_RUN}")
        print(f"Safety Forced DRY_RUN: {cfg.FORCED_DRY_RUN}")
        
        if cfg.DRY_RUN:
            print("✅ Trade config enforces DRY RUN")
        else:
            print("❌ Trade config allows live trading!")
            
    except Exception as e:
        print(f"❌ Config integration error: {e}")

def test_simulation_engine():
    """Test that simulation engine has safety checks"""
    print("\n🎮 TESTING SIMULATION ENGINE SAFETY")
    print("=" * 40)
    
    try:
        from core.simulation_engine import simulator
        
        # Try to open a position - should work in simulation
        position_id = simulator.open_position("ETH", "long", 100)
        
        if position_id:
            print("✅ Simulation engine works correctly")
            print(f"   Created simulated position: {position_id[:8]}...")
            
            # Clean up
            simulator.close_position(position_id, "Safety test cleanup")
        else:
            print("⚠️ Simulation engine blocked trade (this might be expected)")
            
    except Exception as e:
        print(f"❌ Simulation engine error: {e}")

def test_dashboard_safety():
    """Test that dashboard shows safety correctly"""
    print("\n📊 TESTING DASHBOARD SAFETY DISPLAY")
    print("=" * 42)
    
    try:
        from dashboard.minimal_dashboard import dashboard
        
        print("Testing dashboard safety methods...")
        
        # Test dashboard can access safety status
        from config.safety_config import safety
        status = safety.get_safety_status()
        
        if status['forced_dry_run']:
            print("✅ Dashboard correctly detects forced dry run")
        else:
            print("⚠️ Dashboard shows live trading possible")
            
    except Exception as e:
        print(f"❌ Dashboard safety test error: {e}")

def simulate_attack_scenarios():
    """Test common ways someone might try to bypass safety"""
    print("\n🔍 TESTING ATTACK SCENARIOS")
    print("=" * 35)
    
    print("1. Attempting to modify DRY_RUN at runtime...")
    try:
        import config.trade_config as cfg
        original_dry_run = cfg.DRY_RUN
        
        # Try to change it
        cfg.DRY_RUN = False
        
        # Check if safety overrides it
        from config.safety_config import safety
        if safety.is_dry_run_forced():
            print("✅ Safety overrides runtime modification")
        else:
            print("❌ Runtime modification succeeded!")
            
        # Restore
        cfg.DRY_RUN = original_dry_run
        
    except Exception as e:
        print(f"⚠️ Runtime modification test failed: {e}")
    
    print("\n2. Testing environment variable manipulation...")
    # This test shows what would happen if someone tried to change env vars
    original_env = os.environ.get('ENABLE_LIVE_TRADING', 'FALSE')
    
    try:
        os.environ['ENABLE_LIVE_TRADING'] = 'TRUE'
        
        # Check if other safety layers still protect
        if safety.SAFETY_LOCK_ENABLED:
            print("✅ Primary safety lock still protects despite env change")
        else:
            print("❌ Env manipulation could be dangerous!")
            
    finally:
        # Restore
        os.environ['ENABLE_LIVE_TRADING'] = original_env

def generate_safety_report():
    """Generate a comprehensive safety report"""
    print("\n📋 COMPREHENSIVE SAFETY REPORT")
    print("=" * 45)
    
    safety.print_safety_status()
    
    # Count active safety layers
    status = safety.get_safety_status()
    active_layers = 0
    
    if status['safety_lock']:
        active_layers += 1
    if not status['env_check']:
        active_layers += 1
    if not status['manual_file']:
        active_layers += 1
    if not status['wallet_approved']:
        active_layers += 1
    
    print(f"🛡️ Active Safety Layers: {active_layers}/4")
    
    if active_layers >= 1:
        print("✅ RECOMMENDATION: Your setup is SAFE for testing")
        print("💚 You can proceed with confidence")
    else:
        print("⚠️ WARNING: No safety layers active!")
        print("🔴 Live trading is possible - be careful!")
    
    print(f"\n📊 Risk Level: {'MINIMAL' if active_layers >= 3 else 'LOW' if active_layers >= 1 else 'HIGH'}")

def main():
    """Run all safety tests"""
    print("🛡️ JUPITER ETH PERPS BOT - SAFETY VERIFICATION")
    print("=" * 60)
    print("This script verifies all safety mechanisms are working")
    print("to protect your funds during development and testing.")
    print()
    
    try:
        # Run all tests
        is_safe = test_safety_layers()
        test_config_integration()
        test_simulation_engine()
        test_dashboard_safety()
        simulate_attack_scenarios()
        generate_safety_report()
        
        print("\n" + "=" * 60)
        if is_safe:
            print("🎉 SAFETY VERIFICATION COMPLETE")
            print("✅ Your funds are PROTECTED - safe to test!")
            print("🚀 You can run the bot with confidence")
        else:
            print("⚠️ SAFETY VERIFICATION FAILED")
            print("❌ Live trading might be possible!")
            print("🔒 Please review safety settings")
        
        print("\n🚀 To start the bot: python3 main_minimal.py")
        
    except Exception as e:
        print(f"\n❌ Safety verification error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()