#!/usr/bin/env python3
"""
Test Script for Trading Bot Update
Verifies that the v2.0 update works correctly
"""
import sys
import os
import json
from datetime import datetime

def test_version_update():
    """Test that version is updated to 2.0.0"""
    print("🧪 Testing Version Update...")
    
    try:
        from main import PlatformDetector
        
        info = PlatformDetector.detect_platform()
        
        if info.get('version') == '2.0.0':
            print("✅ Version updated to 2.0.0")
            return True
        else:
            print(f"❌ Version not updated. Current: {info.get('version', 'unknown')}")
            return False
    except Exception as e:
        print(f"❌ Version test failed: {e}")
        return False

def test_enhanced_features():
    """Test enhanced features"""
    print("\n🧪 Testing Enhanced Features...")
    
    try:
        from main import UnifiedTradingBot, PlatformDetector
        
        platform_info = PlatformDetector.detect_platform()
        bot = UnifiedTradingBot(platform_info)
        
        # Test performance stats
        stats = bot.get_performance_stats()
        
        required_fields = ['runtime_hours', 'total_trades', 'win_count', 'loss_count', 'win_rate', 'total_pnl']
        missing_fields = [field for field in required_fields if field not in stats]
        
        if not missing_fields:
            print("✅ Enhanced performance tracking working")
            print(f"   Runtime: {stats['runtime_hours']:.2f} hours")
            print(f"   Win Rate: {stats['win_rate']:.1f}%")
            print(f"   Total PnL: ${stats['total_pnl']:.2f}")
            return True
        else:
            print(f"❌ Missing performance fields: {missing_fields}")
            return False
    except Exception as e:
        print(f"❌ Enhanced features test failed: {e}")
        return False

def test_data_export():
    """Test data export functionality"""
    print("\n🧪 Testing Data Export...")
    
    try:
        from main import UnifiedTradingBot, PlatformDetector
        
        platform_info = PlatformDetector.detect_platform()
        bot = UnifiedTradingBot(platform_info)
        
        # Test saving performance data
        bot.save_performance_data()
        
        if os.path.exists('bot_performance.json'):
            with open('bot_performance.json', 'r') as f:
                data = json.load(f)
            
            print("✅ Data export working")
            print(f"   File created: bot_performance.json")
            print(f"   Data fields: {len(data)} fields")
            return True
        else:
            print("❌ Performance data file not created")
            return False
    except Exception as e:
        print(f"❌ Data export test failed: {e}")
        return False

def test_enhanced_display():
    """Test enhanced status display"""
    print("\n🧪 Testing Enhanced Display...")
    
    try:
        from main import UnifiedTradingBot, PlatformDetector
        
        platform_info = PlatformDetector.detect_platform()
        bot = UnifiedTradingBot(platform_info)
        
        # Add some test data
        bot.cycle_count = 10
        bot.balance = 10150.0
        bot.current_eth_price = 3025.50
        bot.price_history = [3000, 3010, 3020, 3015, 3025, 3030, 3028, 3035, 3040, 3038, 3025]
        bot.win_count = 3
        bot.loss_count = 2
        bot.total_pnl = 150.0
        
        # Test display (capture output)
        import io
        from contextlib import redirect_stdout
        
        f = io.StringIO()
        with redirect_stdout(f):
            bot.display_status()
        
        output = f.getvalue()
        
        if 'Win Rate:' in output and 'Runtime:' in output and 'Total PnL:' in output:
            print("✅ Enhanced display working")
            print("   Shows win rate, runtime, and total PnL")
            return True
        else:
            print("❌ Enhanced display missing features")
            print(f"   Output: {output[:200]}...")
            return False
    except Exception as e:
        print(f"❌ Enhanced display test failed: {e}")
        return False

def test_backward_compatibility():
    """Test backward compatibility"""
    print("\n🧪 Testing Backward Compatibility...")
    
    try:
        # Test that old features still work
        from main import UnifiedTradingBot, PlatformDetector
        
        platform_info = PlatformDetector.detect_platform()
        bot = UnifiedTradingBot(platform_info)
        
        # Test basic functionality
        price = bot.get_eth_price()
        signal = bot.generate_signal()
        indicators = bot.calculate_simple_indicators()
        
        if price > 0 and signal and indicators:
            print("✅ Backward compatibility maintained")
            print(f"   Price: ${price:.2f}")
            print(f"   Signal: {signal['action']}")
            print(f"   RSI: {indicators['rsi']:.1f}")
            return True
        else:
            print("❌ Backward compatibility issues")
            return False
    except Exception as e:
        print(f"❌ Backward compatibility test failed: {e}")
        return False

def main():
    """Run all update tests"""
    print("🚀 Testing Trading Bot Update v2.0")
    print("=" * 50)
    
    tests = [
        ("Version Update", test_version_update),
        ("Enhanced Features", test_enhanced_features),
        ("Data Export", test_data_export),
        ("Enhanced Display", test_enhanced_display),
        ("Backward Compatibility", test_backward_compatibility)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🧪 Running: {test_name}")
        if test_func():
            passed += 1
            print(f"✅ {test_name} PASSED")
        else:
            print(f"❌ {test_name} FAILED")
    
    print("\n" + "=" * 50)
    print(f"📊 UPDATE TEST RESULTS: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 ALL UPDATE TESTS PASSED!")
        print("✅ Trading Bot v2.0 is working correctly!")
        print("\n💡 New features available:")
        print("   • Enhanced performance tracking")
        print("   • Win/loss statistics")
        print("   • Data export to JSON")
        print("   • Improved status display")
        print("   • Better error handling")
        print("\n🚀 Ready to use: python main.py")
        sys.exit(0)
    else:
        print(f"\n❌ {total - passed} tests failed")
        print("Check the errors above")
        sys.exit(1)

if __name__ == "__main__":
    main()