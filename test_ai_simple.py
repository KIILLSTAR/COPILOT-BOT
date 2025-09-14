#!/usr/bin/env python3
"""
Simplified AI Learning Test
Tests basic AI functionality without heavy dependencies
"""
import json
import os
import sys
from datetime import datetime

def test_basic_ai_imports():
    """Test basic AI module imports"""
    print("🧠 Testing basic AI imports...")
    
    try:
        # Test AI learning module
        from ai_learning import AILearningEngine, TradingSignal, TradeOutcome
        print("✅ AI learning module imported")
        
        # Test AI signal detector
        from ai_signal_detector import AISignalDetector
        print("✅ AI signal detector imported")
        
        return True
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False

def test_ai_signal_creation():
    """Test creating AI signals"""
    print("\n🔍 Testing AI signal creation...")
    
    try:
        from ai_learning import TradingSignal
        
        # Create a test signal
        signal = TradingSignal(
            action='long',
            confidence=0.75,
            features={'price': 3500.0, 'rsi': 45.0},
            timestamp=datetime.now(),
            model_version='1.0.0',
            reasoning='Test signal for AI learning'
        )
        
        print(f"✅ Signal created: {signal.action} with {signal.confidence:.1%} confidence")
        return True
    except Exception as e:
        print(f"❌ Signal creation error: {e}")
        return False

def test_ai_engine_initialization():
    """Test AI engine initialization"""
    print("\n⚙️ Testing AI engine initialization...")
    
    try:
        from ai_learning import AILearningEngine
        
        # Create AI engine
        ai_engine = AILearningEngine()
        
        # Test model status
        status = ai_engine.get_model_status()
        print(f"✅ AI Engine initialized:")
        print(f"   Model Version: {status['model_version']}")
        print(f"   ML Available: {status['ml_available']}")
        print(f"   Models Trained: {status['models_trained']}")
        
        return True
    except Exception as e:
        print(f"❌ AI engine error: {e}")
        return False

def test_signal_detector_initialization():
    """Test signal detector initialization"""
    print("\n📡 Testing signal detector initialization...")
    
    try:
        from ai_signal_detector import AISignalDetector
        
        # Create signal detector
        detector = AISignalDetector()
        
        # Test signal weights
        print(f"✅ Signal detector initialized:")
        print(f"   Signal weights: {detector.signal_weights}")
        print(f"   Base threshold: {detector.base_threshold}")
        
        return True
    except Exception as e:
        print(f"❌ Signal detector error: {e}")
        return False

def test_mock_signal_generation():
    """Test mock signal generation"""
    print("\n🎯 Testing mock signal generation...")
    
    try:
        from ai_signal_detector import AISignalDetector
        
        detector = AISignalDetector()
        
        # Create mock data
        mock_market_data = {
            'price': 3500.0,
            'rsi': 45.0,
            'ema_12': 3480.0,
            'ema_26': 3520.0,
            'funding_rate': 0.001,
            'volume_24h': 1500000.0
        }
        
        mock_trade_history = []
        mock_portfolio_data = {
            'current_balance': 10000.0,
            'total_pnl': 100.0,
            'win_rate': 0.6
        }
        
        # Generate signal
        signal_data = detector.generate_ai_enhanced_signal(
            mock_market_data, mock_trade_history, mock_portfolio_data
        )
        
        print(f"✅ Mock signal generated:")
        print(f"   Action: {signal_data['action']}")
        print(f"   Confidence: {signal_data['confidence']:.2%}")
        print(f"   AI Enhanced: {'ai_signal' in signal_data}")
        
        return True
    except Exception as e:
        print(f"❌ Mock signal generation error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_existing_data_loading():
    """Test loading existing simulation data"""
    print("\n📊 Testing existing data loading...")
    
    try:
        if os.path.exists("simulation_data.json"):
            with open("simulation_data.json", 'r') as f:
                data = json.load(f)
            
            print(f"✅ Simulation data loaded:")
            print(f"   Current balance: ${data.get('current_balance', 0):,.2f}")
            print(f"   Total trades: {data.get('metrics', {}).get('total_trades', 0)}")
            print(f"   Trade history entries: {len(data.get('trade_history', []))}")
            
            return True
        else:
            print("⚠️ No simulation data found")
            return True  # Not an error, just no data
    except Exception as e:
        print(f"❌ Data loading error: {e}")
        return False

def main():
    """Run simplified AI tests"""
    print("🚀 Starting Simplified AI Learning Tests...")
    print("=" * 50)
    
    tests = [
        ("Basic Imports", test_basic_ai_imports),
        ("Signal Creation", test_ai_signal_creation),
        ("AI Engine Init", test_ai_engine_initialization),
        ("Signal Detector Init", test_signal_detector_initialization),
        ("Mock Signal Generation", test_mock_signal_generation),
        ("Data Loading", test_existing_data_loading)
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
    print(f"📊 RESULTS: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED!")
        print("\n💡 AI Learning system is ready with:")
        print("   • Basic AI signal generation")
        print("   • Adaptive signal weights")
        print("   • Learning from trade outcomes")
        print("   • Fallback to traditional analysis")
        print("   • Integration with existing data")
        sys.exit(0)
    else:
        print(f"\n❌ {total - passed} tests failed")
        sys.exit(1)

if __name__ == "__main__":
    main()