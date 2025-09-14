#!/usr/bin/env python3
"""
Test Script for Unified Main
Tests the unified trading bot functionality
"""
import sys
import os

def test_platform_detection():
    """Test platform detection"""
    print("🧪 Testing Platform Detection...")
    
    try:
        from unified_main import PlatformDetector
        
        info = PlatformDetector.detect_platform()
        
        print(f"✅ Platform Detection:")
        print(f"   OS: {info['os']}")
        print(f"   Mobile: {info['is_mobile']}")
        print(f"   Internet: {info['has_internet']}")
        print(f"   Display: {info['has_display']}")
        print(f"   Limited: {info['is_limited']}")
        print(f"   Recommended Mode: {info['recommended_mode']}")
        
        return True
    except Exception as e:
        print(f"❌ Platform detection failed: {e}")
        return False

def test_bot_initialization():
    """Test bot initialization"""
    print("\n🧪 Testing Bot Initialization...")
    
    try:
        from unified_main import UnifiedTradingBot, PlatformDetector
        
        platform_info = PlatformDetector.detect_platform()
        bot = UnifiedTradingBot(platform_info)
        
        print(f"✅ Bot Initialized:")
        print(f"   Balance: ${bot.balance:,.2f}")
        print(f"   AI Enabled: {bot.ai_enabled}")
        print(f"   Platform Mode: {bot.platform_info['recommended_mode']}")
        
        return True
    except Exception as e:
        print(f"❌ Bot initialization failed: {e}")
        return False

def test_price_fetching():
    """Test price fetching"""
    print("\n🧪 Testing Price Fetching...")
    
    try:
        from unified_main import UnifiedTradingBot, PlatformDetector
        
        platform_info = PlatformDetector.detect_platform()
        bot = UnifiedTradingBot(platform_info)
        
        price = bot.get_eth_price()
        
        print(f"✅ Price Fetching:")
        print(f"   ETH Price: ${price:,.2f}")
        print(f"   Mode: {bot.platform_info['recommended_mode']}")
        
        return True
    except Exception as e:
        print(f"❌ Price fetching failed: {e}")
        return False

def test_signal_generation():
    """Test signal generation"""
    print("\n🧪 Testing Signal Generation...")
    
    try:
        from unified_main import UnifiedTradingBot, PlatformDetector
        
        platform_info = PlatformDetector.detect_platform()
        bot = UnifiedTradingBot(platform_info)
        
        # Get a price first
        bot.current_eth_price = bot.get_eth_price()
        
        signal = bot.generate_signal()
        
        print(f"✅ Signal Generation:")
        print(f"   Action: {signal['action']}")
        print(f"   Confidence: {signal['confidence']:.1%}")
        print(f"   Source: {signal['source']}")
        print(f"   Reasoning: {signal['reasoning']}")
        
        return True
    except Exception as e:
        print(f"❌ Signal generation failed: {e}")
        return False

def test_indicators():
    """Test technical indicators"""
    print("\n🧪 Testing Technical Indicators...")
    
    try:
        from unified_main import UnifiedTradingBot, PlatformDetector
        
        platform_info = PlatformDetector.detect_platform()
        bot = UnifiedTradingBot(platform_info)
        
        # Add some price history
        bot.price_history = [3000, 3010, 3020, 3015, 3025, 3030, 3028, 3035, 3040, 3038]
        
        indicators = bot.calculate_simple_indicators()
        
        print(f"✅ Technical Indicators:")
        print(f"   RSI: {indicators['rsi']:.1f}")
        print(f"   Trend: {indicators['trend']:.3f}")
        print(f"   Volatility: {indicators['volatility']:.3f}")
        
        return True
    except Exception as e:
        print(f"❌ Indicators failed: {e}")
        return False

def test_trade_execution():
    """Test trade execution"""
    print("\n🧪 Testing Trade Execution...")
    
    try:
        from unified_main import UnifiedTradingBot, PlatformDetector
        
        platform_info = PlatformDetector.detect_platform()
        bot = UnifiedTradingBot(platform_info)
        
        # Create a test signal
        signal = {
            'action': 'long',
            'confidence': 0.8,
            'reasoning': 'Test signal'
        }
        
        initial_balance = bot.balance
        bot.current_eth_price = 3000.0
        
        # Execute trade
        executed = bot.execute_trade(signal)
        
        print(f"✅ Trade Execution:")
        print(f"   Executed: {executed}")
        print(f"   Initial Balance: ${initial_balance:,.2f}")
        print(f"   Final Balance: ${bot.balance:,.2f}")
        print(f"   Trade History: {len(bot.trade_history)} trades")
        
        return True
    except Exception as e:
        print(f"❌ Trade execution failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Testing Unified Trading Bot")
    print("=" * 50)
    
    tests = [
        ("Platform Detection", test_platform_detection),
        ("Bot Initialization", test_bot_initialization),
        ("Price Fetching", test_price_fetching),
        ("Signal Generation", test_signal_generation),
        ("Technical Indicators", test_indicators),
        ("Trade Execution", test_trade_execution)
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
    print(f"📊 TEST RESULTS: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED!")
        print("✅ Unified trading bot is working correctly!")
        print("\n💡 Ready to use:")
        print("   python main.py")
        sys.exit(0)
    else:
        print(f"\n❌ {total - passed} tests failed")
        print("Check the errors above")
        sys.exit(1)

if __name__ == "__main__":
    main()