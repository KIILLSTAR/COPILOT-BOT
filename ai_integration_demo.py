#!/usr/bin/env python3
"""
AI Integration Demo
Demonstrates how the AI learning system integrates with the existing trading bot
"""
import json
import time
from datetime import datetime
from ai_standalone import (
    initialize_standalone_ai_learning, 
    get_standalone_ai_signal, 
    learn_from_trade_standalone,
    standalone_ai_engine
)

def demo_ai_learning_integration():
    """Demonstrate AI learning integration"""
    print("🚀 AI Learning Integration Demo")
    print("=" * 50)
    
    # Step 1: Initialize AI learning with existing data
    print("\n1️⃣ Initializing AI Learning...")
    initialize_standalone_ai_learning("simulation_data.json")
    
    # Step 2: Generate AI signals
    print("\n2️⃣ Generating AI Trading Signals...")
    
    # Mock market data (in real implementation, this would come from market APIs)
    market_data = {
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
    
    # Mock trade history (in real implementation, this would come from simulation engine)
    trade_history = [
        {
            'realized_pnl': 50.0,
            'entry_time': '2025-01-01T10:00:00Z',
            'exit_time': '2025-01-01T12:00:00Z',
            'status': 'closed'
        },
        {
            'realized_pnl': -25.0,
            'entry_time': '2025-01-01T14:00:00Z',
            'exit_time': '2025-01-01T16:00:00Z',
            'status': 'closed'
        }
    ]
    
    # Mock portfolio data (in real implementation, this would come from simulation engine)
    portfolio_data = {
        'current_balance': 10000.0,
        'total_pnl': 100.0,
        'win_rate': 0.6,
        'positions': {},
        'total_trades': 10
    }
    
    # Generate AI signal
    ai_signal = get_standalone_ai_signal(market_data, trade_history, portfolio_data)
    
    print(f"✅ AI Signal Generated:")
    print(f"   Action: {ai_signal.action.upper()}")
    print(f"   Confidence: {ai_signal.confidence:.1%}")
    print(f"   Reasoning: {ai_signal.reasoning}")
    print(f"   Features Used: {len(ai_signal.features)} market indicators")
    
    # Step 3: Simulate trade execution and learning
    print("\n3️⃣ Simulating Trade Execution and Learning...")
    
    # Simulate trade outcome based on signal
    if ai_signal.action == 'long':
        # Simulate a profitable long trade
        trade_outcome = {
            'entry_price': 3500.0,
            'exit_price': 3550.0,
            'realized_pnl': 50.0,
            'duration': 2.0,
            'market_conditions': market_data
        }
        print("📈 Simulated LONG trade: +$50 profit")
    elif ai_signal.action == 'short':
        # Simulate a profitable short trade
        trade_outcome = {
            'entry_price': 3500.0,
            'exit_price': 3450.0,
            'realized_pnl': 50.0,
            'duration': 2.0,
            'market_conditions': market_data
        }
        print("📉 Simulated SHORT trade: +$50 profit")
    else:
        # Simulate holding (no trade)
        trade_outcome = {
            'entry_price': 3500.0,
            'exit_price': 3500.0,
            'realized_pnl': 0.0,
            'duration': 0.0,
            'market_conditions': market_data
        }
        print("⏸️ Simulated HOLD: No trade executed")
    
    # Learn from the outcome
    learn_from_trade_standalone(ai_signal, trade_outcome)
    print("🧠 AI learned from trade outcome")
    
    # Step 4: Show AI model status
    print("\n4️⃣ AI Model Status:")
    status = standalone_ai_engine.get_model_status()
    
    print(f"   Model Version: {status['model_version']}")
    print(f"   Models Trained: {status['models_trained']}")
    print(f"   Total Predictions: {status['performance']['total_predictions']}")
    print(f"   Correct Predictions: {status['performance']['correct_predictions']}")
    print(f"   Total Outcomes: {status['total_outcomes']}")
    
    if status['performance']['total_predictions'] > 0:
        accuracy = status['performance']['correct_predictions'] / status['performance']['total_predictions']
        print(f"   Current Accuracy: {accuracy:.1%}")
    
    # Step 5: Demonstrate adaptive learning
    print("\n5️⃣ Demonstrating Adaptive Learning...")
    
    # Generate multiple signals to show learning
    print("🔄 Generating multiple signals to demonstrate learning...")
    
    for i in range(3):
        # Vary market conditions slightly
        market_data['price'] += 10 * (i - 1)  # Simulate price movement
        market_data['rsi'] += 5 * (i - 1)     # Simulate RSI change
        
        # Generate new signal
        new_signal = get_standalone_ai_signal(market_data, trade_history, portfolio_data)
        
        print(f"   Signal {i+1}: {new_signal.action.upper()} (confidence: {new_signal.confidence:.1%})")
        
        # Simulate outcome and learn
        if new_signal.action != 'hold':
            outcome = {
                'entry_price': market_data['price'],
                'exit_price': market_data['price'] + (20 if new_signal.action == 'long' else -20),
                'realized_pnl': 20.0,
                'duration': 1.0,
                'market_conditions': market_data
            }
            learn_from_trade_standalone(new_signal, outcome)
    
    print("✅ AI has learned from multiple trade outcomes")
    
    # Final status
    final_status = standalone_ai_engine.get_model_status()
    print(f"\n📊 Final AI Status:")
    print(f"   Total Predictions: {final_status['performance']['total_predictions']}")
    print(f"   Total Outcomes: {final_status['total_outcomes']}")
    
    print("\n🎉 AI Learning Integration Demo Complete!")
    print("\n💡 Key Benefits Demonstrated:")
    print("   • AI learns from existing trade history")
    print("   • Generates intelligent signals with confidence scores")
    print("   • Adapts based on trade outcomes")
    print("   • Provides human-readable reasoning")
    print("   • Integrates seamlessly with existing bot infrastructure")
    print("   • No external dependencies required")

def show_integration_instructions():
    """Show how to integrate AI learning into the main bot"""
    print("\n" + "=" * 60)
    print("🔧 INTEGRATION INSTRUCTIONS")
    print("=" * 60)
    
    print("""
To integrate AI learning into your existing trading bot:

1. Replace signal detection in main.py:
   ```python
   # OLD:
   from strategy.signal_detector import run_signal_loop
   signal_result = run_signal_loop(cfg)
   
   # NEW:
   from ai_standalone import get_standalone_ai_signal
   signal_result = get_standalone_ai_signal(market_data, trade_history, portfolio_data)
   ```

2. Add learning after each trade:
   ```python
   from ai_standalone import learn_from_trade_standalone
   
   # After trade completion:
   learn_from_trade_standalone(signal, trade_outcome)
   ```

3. Initialize AI learning at startup:
   ```python
   from ai_standalone import initialize_standalone_ai_learning
   
   # At bot startup:
   initialize_standalone_ai_learning("simulation_data.json")
   ```

4. Monitor AI performance:
   ```python
   from ai_standalone import standalone_ai_engine
   
   status = standalone_ai_engine.get_model_status()
   print(f"AI Accuracy: {status['performance']['accuracy']:.1%}")
   ```

The AI system will:
✅ Learn from your existing trade history
✅ Adapt strategy weights based on performance
✅ Improve signal accuracy over time
✅ Provide confidence scores and reasoning
✅ Work with your existing safety infrastructure
✅ Require no external dependencies
""")

def main():
    """Run the AI integration demo"""
    try:
        demo_ai_learning_integration()
        show_integration_instructions()
    except Exception as e:
        print(f"❌ Demo error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()