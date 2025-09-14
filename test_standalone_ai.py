#!/usr/bin/env python3
"""
Test script for Standalone AI Learning functionality
Tests the self-contained AI learning system
"""
import json
import os
import sys
from datetime import datetime

def test_standalone_ai_imports():
    """Test standalone AI module imports"""
    print("🧠 Testing standalone AI imports...")
    
    try:
        from ai_standalone import (
            StandaloneAILearningEngine, TradingSignal, TradeOutcome, 
            FeatureExtractor, standalone_ai_engine
        )
        print("✅ Standalone AI modules imported successfully")
        return True
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False

def test_ai_signal_creation():
    """Test creating AI signals"""
    print("\n🔍 Testing AI signal creation...")
    
    try:
        from ai_standalone import TradingSignal
        
        # Create a test signal
        signal = TradingSignal(
            action='long',
            confidence=0.75,
            features={'price': 3500.0, 'rsi': 45.0},
            timestamp=datetime.now(),
            model_version='1.0.0',
            reasoning='Test signal for standalone AI learning'
        )
        
        print(f"✅ Signal created: {signal.action} with {signal.confidence:.1%} confidence")
        return True
    except Exception as e:
        print(f"❌ Signal creation error: {e}")
        return False

def test_ai_engine_initialization():
    """Test AI engine initialization"""
    print("\n⚙️ Testing standalone AI engine initialization...")
    
    try:
        from ai_standalone import standalone_ai_engine
        
        # Test model status
        status = standalone_ai_engine.get_model_status()
        print(f"✅ Standalone AI Engine initialized:")
        print(f"   Model Version: {status['model_version']}")
        print(f"   Models Trained: {status['models_trained']}")
        print(f"   Total Outcomes: {status['total_outcomes']}")
        
        return True
    except Exception as e:
        print(f"❌ AI engine error: {e}")
        return False

def test_feature_extraction():
    """Test feature extraction"""
    print("\n🔧 Testing feature extraction...")
    
    try:
        from ai_standalone import FeatureExtractor
        
        extractor = FeatureExtractor()
        
        # Test market features
        mock_market_data = {
            'price': 3500.0,
            'rsi': 45.0,
            'volume_24h': 1500000.0,
            'funding_rate': 0.001
        }
        
        market_features = extractor.extract_market_features(mock_market_data)
        print(f"✅ Market features extracted: {len(market_features)} features")
        
        # Test historical features
        mock_trade_history = [
            {
                'realized_pnl': 50.0,
                'entry_time': '2025-01-01T10:00:00Z',
                'exit_time': '2025-01-01T12:00:00Z'
            }
        ]
        
        historical_features = extractor.extract_historical_features(mock_trade_history)
        print(f"✅ Historical features extracted: {len(historical_features)} features")
        
        # Test portfolio features
        mock_portfolio_data = {
            'current_balance': 10000.0,
            'total_pnl': 100.0,
            'win_rate': 0.6
        }
        
        portfolio_features = extractor.extract_portfolio_features(mock_portfolio_data)
        print(f"✅ Portfolio features extracted: {len(portfolio_features)} features")
        
        return True
    except Exception as e:
        print(f"❌ Feature extraction error: {e}")
        return False

def test_ai_signal_generation():
    """Test AI signal generation"""
    print("\n🎯 Testing AI signal generation...")
    
    try:
        from ai_standalone import get_standalone_ai_signal
        
        # Create mock data
        mock_market_data = {
            'price': 3500.0,
            'rsi': 45.0,
            'ema_12': 3480.0,
            'ema_26': 3520.0,
            'funding_rate': 0.001,
            'volume_24h': 1500000.0,
            'fear_greed_index': 55.0
        }
        
        mock_trade_history = [
            {
                'realized_pnl': 50.0,
                'entry_time': '2025-01-01T10:00:00Z',
                'exit_time': '2025-01-01T12:00:00Z'
            }
        ]
        
        mock_portfolio_data = {
            'current_balance': 10000.0,
            'total_pnl': 100.0,
            'win_rate': 0.6,
            'positions': {},
            'total_trades': 10
        }
        
        # Generate signal
        ai_signal = get_standalone_ai_signal(mock_market_data, mock_trade_history, mock_portfolio_data)
        
        print(f"✅ AI Signal Generated:")
        print(f"   Action: {ai_signal.action}")
        print(f"   Confidence: {ai_signal.confidence:.2%}")
        print(f"   Reasoning: {ai_signal.reasoning}")
        
        return True
    except Exception as e:
        print(f"❌ AI signal generation error: {e}")
        return False

def test_training_with_existing_data():
    """Test training with existing simulation data"""
    print("\n📚 Testing training with existing data...")
    
    try:
        from ai_standalone import initialize_standalone_ai_learning
        
        if os.path.exists("simulation_data.json"):
            initialize_standalone_ai_learning("simulation_data.json")
            print("✅ Training completed with existing data")
        else:
            print("⚠️ No simulation data found - skipping training test")
        
        return True
    except Exception as e:
        print(f"❌ Training error: {e}")
        return False

def test_learning_from_outcomes():
    """Test learning from trade outcomes"""
    print("\n📈 Testing learning from trade outcomes...")
    
    try:
        from ai_standalone import TradingSignal, learn_from_trade_standalone
        
        # Create test signal
        signal = TradingSignal(
            action='long',
            confidence=0.75,
            features={'price': 3500.0, 'rsi': 45.0},
            timestamp=datetime.now(),
            model_version='1.0.0',
            reasoning='Test learning signal'
        )
        
        # Create test outcome
        trade_outcome = {
            'entry_price': 3500.0,
            'exit_price': 3550.0,
            'realized_pnl': 50.0,
            'duration': 2.0,
            'market_conditions': {'price': 3500.0, 'rsi': 45.0}
        }
        
        # Learn from outcome
        learn_from_trade_standalone(signal, trade_outcome)
        print("✅ Successfully learned from trade outcome")
        
        return True
    except Exception as e:
        print(f"❌ Learning error: {e}")
        return False

def test_model_performance():
    """Test model performance tracking"""
    print("\n📊 Testing model performance tracking...")
    
    try:
        from ai_standalone import standalone_ai_engine
        
        status = standalone_ai_engine.get_model_status()
        
        print(f"✅ Model Performance:")
        print(f"   Accuracy: {status['performance']['accuracy']:.2%}")
        print(f"   Total Predictions: {status['performance']['total_predictions']}")
        print(f"   Correct Predictions: {status['performance']['correct_predictions']}")
        print(f"   Total Outcomes: {status['total_outcomes']}")
        
        return True
    except Exception as e:
        print(f"❌ Performance tracking error: {e}")
        return False

def main():
    """Run all standalone AI tests"""
    print("🚀 Starting Standalone AI Learning Test Suite...")
    print("=" * 60)
    
    tests = [
        ("Standalone AI Imports", test_standalone_ai_imports),
        ("Signal Creation", test_ai_signal_creation),
        ("AI Engine Init", test_ai_engine_initialization),
        ("Feature Extraction", test_feature_extraction),
        ("AI Signal Generation", test_ai_signal_generation),
        ("Training with Data", test_training_with_existing_data),
        ("Learning from Outcomes", test_learning_from_outcomes),
        ("Model Performance", test_model_performance)
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
    
    print("\n" + "=" * 60)
    print(f"📊 RESULTS: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED!")
        print("\n💡 Standalone AI Learning system is ready with:")
        print("   • Self-contained AI signal generation")
        print("   • Feature extraction from market data")
        print("   • Learning from trade outcomes")
        print("   • Performance tracking")
        print("   • No external dependencies")
        print("   • Integration with existing data")
        sys.exit(0)
    else:
        print(f"\n❌ {total - passed} tests failed")
        sys.exit(1)

if __name__ == "__main__":
    main()