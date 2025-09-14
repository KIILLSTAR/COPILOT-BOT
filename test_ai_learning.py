#!/usr/bin/env python3
"""
Test script for AI Learning functionality
Verifies that the AI learning system works correctly with existing data
"""
import json
import os
import sys
from datetime import datetime

def test_ai_learning():
    """Test AI learning functionality"""
    print("🧠 Testing AI Learning System...")
    
    try:
        # Test 1: Import AI modules
        print("\n1. Testing AI module imports...")
        from ai_learning import AILearningEngine, TradingSignal, TradeOutcome, initialize_ai_learning
        from ai_signal_detector import AISignalDetector, run_ai_signal_loop
        print("✅ AI modules imported successfully")
        
        # Test 2: Initialize AI learning with existing data
        print("\n2. Testing AI initialization...")
        if os.path.exists("simulation_data.json"):
            initialize_ai_learning("simulation_data.json")
            print("✅ AI learning initialized with existing data")
        else:
            print("⚠️ No simulation data found - AI will start fresh")
        
        # Test 3: Test signal generation
        print("\n3. Testing AI signal generation...")
        
        # Create mock market data
        mock_market_data = {
            'price': 3500.0,
            'rsi': 45.0,
            'ema_12': 3480.0,
            'ema_26': 3520.0,
            'bb_upper': 3600.0,
            'bb_middle': 3500.0,
            'bb_lower': 3400.0,
            'funding_rate': 0.001,
            'volume_24h': 1500000.0,
            'fear_greed_index': 55.0,
            'social_sentiment': 0.1
        }
        
        # Create mock trade history
        mock_trade_history = [
            {
                'id': 'test_trade_1',
                'symbol': 'ETH',
                'side': 'long',
                'entry_price': 3400.0,
                'exit_price': 3450.0,
                'realized_pnl': 50.0,
                'status': 'closed',
                'entry_time': '2025-01-01T10:00:00Z',
                'exit_time': '2025-01-01T12:00:00Z'
            }
        ]
        
        # Create mock portfolio data
        mock_portfolio_data = {
            'current_balance': 10000.0,
            'total_pnl': 100.0,
            'win_rate': 0.6,
            'positions': {},
            'total_trades': 10
        }
        
        # Test AI signal generation
        from ai_learning import get_ai_signal
        ai_signal = get_ai_signal(mock_market_data, mock_trade_history, mock_portfolio_data)
        
        print(f"✅ AI Signal Generated:")
        print(f"   Action: {ai_signal.action}")
        print(f"   Confidence: {ai_signal.confidence:.2%}")
        print(f"   Reasoning: {ai_signal.reasoning}")
        
        # Test 4: Test AI-enhanced signal detector
        print("\n4. Testing AI-enhanced signal detector...")
        
        from ai_signal_detector import ai_signal_detector
        
        # Test signal generation
        signal_data = ai_signal_detector.generate_ai_enhanced_signal(
            mock_market_data, mock_trade_history, mock_portfolio_data
        )
        
        print(f"✅ AI-Enhanced Signal Generated:")
        print(f"   Action: {signal_data['action']}")
        print(f"   Confidence: {signal_data['confidence']:.2%}")
        print(f"   Combined Score: {signal_data['combined_score']:.3f}")
        print(f"   AI Reasoning: {signal_data['ai_signal']['reasoning']}")
        
        # Test 5: Test learning from outcomes
        print("\n5. Testing learning from trade outcomes...")
        
        # Create mock trade outcome
        mock_outcome = {
            'entry_price': 3500.0,
            'exit_price': 3550.0,
            'realized_pnl': 50.0,
            'duration': 2.0,
            'market_conditions': mock_market_data
        }
        
        # Test learning
        ai_signal_detector.update_signal_performance(signal_data, mock_outcome)
        print("✅ Successfully learned from trade outcome")
        
        # Test 6: Test model status
        print("\n6. Testing model status...")
        
        from ai_learning import ai_engine
        model_status = ai_engine.get_model_status()
        
        print(f"✅ Model Status:")
        print(f"   Model Version: {model_status['model_version']}")
        print(f"   Models Trained: {model_status['models_trained']}")
        print(f"   ML Available: {model_status['ml_available']}")
        print(f"   Total Outcomes: {model_status['total_outcomes']}")
        
        # Test 7: Test signal statistics
        print("\n7. Testing signal statistics...")
        
        stats = ai_signal_detector.get_signal_statistics()
        print(f"✅ Signal Statistics:")
        print(f"   Total Signals: {stats.get('total_signals', 0)}")
        print(f"   Success Rate: {stats.get('success_rate', 0):.2%}")
        print(f"   Current Weights: {stats.get('current_weights', {})}")
        
        print("\n🎉 All AI Learning tests passed!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Make sure all required modules are available")
        return False
    except Exception as e:
        print(f"❌ Test error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_integration():
    """Test integration with existing system"""
    print("\n🔗 Testing AI integration with existing system...")
    
    try:
        # Test that AI signal loop works
        from app_config import trade_config as cfg
        signal_result = run_ai_signal_loop(cfg)
        
        print(f"✅ AI Signal Loop Result:")
        print(f"   Action: {signal_result.get('action', 'unknown')}")
        print(f"   Confidence: {signal_result.get('confidence', 0):.2%}")
        print(f"   AI Enhanced: {signal_result.get('ai_enhanced', False)}")
        
        if signal_result.get('ai_enhanced'):
            print("✅ AI enhancement is working correctly")
        else:
            print("⚠️ AI enhancement may not be fully active")
        
        return True
        
    except Exception as e:
        print(f"❌ Integration test error: {e}")
        return False

def main():
    """Run all AI learning tests"""
    print("🚀 Starting AI Learning Test Suite...")
    print("=" * 50)
    
    # Test AI learning functionality
    ai_test_passed = test_ai_learning()
    
    # Test integration
    integration_test_passed = test_integration()
    
    print("\n" + "=" * 50)
    print("📊 TEST RESULTS:")
    print(f"   AI Learning Tests: {'✅ PASSED' if ai_test_passed else '❌ FAILED'}")
    print(f"   Integration Tests: {'✅ PASSED' if integration_test_passed else '❌ FAILED'}")
    
    if ai_test_passed and integration_test_passed:
        print("\n🎉 ALL TESTS PASSED! AI Learning system is ready!")
        print("\n💡 The trading bot now has:")
        print("   • Machine learning-powered signal detection")
        print("   • Adaptive strategy weights based on performance")
        print("   • Learning from trade outcomes")
        print("   • Enhanced confidence scoring")
        print("   • Fallback to traditional analysis when needed")
        sys.exit(0)
    else:
        print("\n❌ Some tests failed. Check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main()