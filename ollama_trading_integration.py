#!/usr/bin/env python3
"""
Ollama Trading Assistant Integration
Connects Ollama AI assistant to your existing COPILOT-BOT infrastructure
Reuses market data fetching, portfolio status, and CLI patterns
"""
import sys
import os
from typing import Dict, Any, Optional, List
from datetime import datetime

# Import your existing trading bot components
try:
    from core.price_fetcher import price_fetcher
    from ai_signal_detector import AISignalDetector
    from core.simulation_engine import simulator
    from core.drift_client import DriftClient
    from app_config import trade_config as cfg
    from app_logger import _write_log
    HAS_EXISTING_BOT = True
except ImportError as e:
    print(f"⚠️ Some imports failed: {e}")
    print("💡 This module works best with your full trading bot, but can run standalone")
    HAS_EXISTING_BOT = False

# Import Ollama components
from trading_ai_assistant import TradingAIAssistant
from ollama_client import OllamaClient


class IntegratedTradingAssistant:
    """
    Trading AI Assistant that integrates with your existing COPILOT-BOT infrastructure
    Reuses market data, portfolio data, and configuration from your existing system
    """
    
    def __init__(self, 
                 ollama_url: str = "http://localhost:11434",
                 model_name: str = "llama3.2",
                 enable_comet: bool = False):
        """
        Initialize integrated assistant
        
        Args:
            ollama_url: Ollama server URL
            model_name: Model to use
            enable_comet: Enable Comet ML tracking
        """
        self.assistant = TradingAIAssistant(
            ollama_url=ollama_url,
            model_name=model_name,
            enable_comet=enable_comet
        )
        
        # Initialize existing bot components if available
        if HAS_EXISTING_BOT:
            try:
                self.signal_detector = AISignalDetector()
                self.drift_client = DriftClient()
                print("✅ Connected to existing trading bot infrastructure")
            except Exception as e:
                print(f"⚠️ Could not initialize all components: {e}")
                self.signal_detector = None
                self.drift_client = None
        else:
            self.signal_detector = None
            self.drift_client = None
    
    def get_live_market_data(self) -> Dict[str, Any]:
        """
        Get live market data using your existing infrastructure
        Reuses AISignalDetector.get_market_data() method
        """
        if self.signal_detector:
            try:
                return self.signal_detector.get_market_data()
            except Exception as e:
                print(f"⚠️ Error getting market data: {e}")
                return self._get_basic_market_data()
        else:
            return self._get_basic_market_data()
    
    def _get_basic_market_data(self) -> Dict[str, Any]:
        """Fallback method if existing infrastructure unavailable"""
        try:
            if HAS_EXISTING_BOT:
                price = price_fetcher.get_eth_price()
            else:
                price = 3500.0  # Fallback
        except:
            price = 3500.0
        
        return {
            'price': price,
            'rsi': 50.0,
            'volume_24h': 1000000.0,
            'funding_rate': 0.001
        }
    
    def get_portfolio_status(self) -> Dict[str, Any]:
        """
        Get portfolio status using your existing simulation engine
        Reuses simulator.get_portfolio_summary() method
        """
        if HAS_EXISTING_BOT and simulator:
            try:
                portfolio = simulator.get_portfolio_summary()
                return {
                    'balance': portfolio.get('balance', 0),
                    'total_pnl': portfolio.get('total_pnl', 0),
                    'open_positions': portfolio.get('open_positions', 0),
                    'total_trades': portfolio.get('total_trades', 0),
                    'win_rate': portfolio.get('win_rate', 0),
                    'roi': portfolio.get('roi', 0)
                }
            except Exception as e:
                print(f"⚠️ Error getting portfolio: {e}")
                return self._get_basic_portfolio()
        else:
            return self._get_basic_portfolio()
    
    def _get_basic_portfolio(self) -> Dict[str, Any]:
        """Fallback portfolio data"""
        return {
            'balance': 10000.0,
            'total_pnl': 0.0,
            'open_positions': 0,
            'total_trades': 0,
            'win_rate': 0.0,
            'roi': 0.0
        }
    
    def get_trade_history(self) -> List[Dict[str, Any]]:
        """
        Get recent trade history from simulation engine
        """
        if HAS_EXISTING_BOT and simulator:
            try:
                # Get recent closed positions
                history = []
                for trade in simulator.trade_history[-10:]:  # Last 10 trades
                    if hasattr(trade, 'realized_pnl'):
                        history.append({
                            'realized_pnl': trade.realized_pnl,
                            'entry_time': trade.entry_time,
                            'exit_time': trade.exit_time,
                            'status': trade.status,
                            'side': getattr(trade, 'side', 'unknown'),
                            'entry_price': trade.entry_price
                        })
                return history
            except Exception as e:
                print(f"⚠️ Error getting trade history: {e}")
                return []
        else:
            return []
    
    def analyze_and_recommend(self) -> Dict[str, Any]:
        """
        Complete analysis using existing market data + Ollama AI
        This is the main method you'll call for trading decisions
        """
        print("📊 Gathering live market data...")
        market_data = self.get_live_market_data()
        
        print("💰 Getting portfolio status...")
        portfolio = self.get_portfolio_status()
        
        print("📜 Loading trade history...")
        trade_history = self.get_trade_history()
        
        print("🤖 AI analyzing data and generating recommendation...")
        result = self.assistant.analyze_live_data(
            market_data=market_data,
            portfolio=portfolio,
            trade_history=trade_history
        )
        
        # Log to your existing logger if available
        if HAS_EXISTING_BOT:
            try:
                _write_log("AI_ASSISTANT", 
                          f"Recommendation: {result['recommendation']['action']} "
                          f"(Confidence: {result['recommendation']['confidence']}/10)")
            except:
                pass
        
        return result
    
    def get_quick_recommendation(self) -> str:
        """
        Get a fast recommendation for quick decision-making
        Uses your existing market data infrastructure
        """
        market_data = self.get_live_market_data()
        
        indicators = {
            'rsi': market_data.get('rsi', 50.0),
            'ema_trend': 'bullish' if market_data.get('price', 0) > market_data.get('ema_12', 0) else 'bearish',
            'volume': 'high' if market_data.get('volume_24h', 0) > 1000000 else 'low'
        }
        
        return self.assistant.get_quick_recommendation(
            price=market_data.get('price', 3500.0),
            indicators=indicators
        )


def integrated_cli_menu():
    """
    CLI interface for the integrated Ollama trading assistant
    Reuses patterns from app_cli.py
    """
    print("🚀 Ollama Trading AI Assistant")
    print("=" * 50)
    
    # Test Ollama connection
    print("\n1️⃣ Testing Ollama connection...")
    try:
        client = OllamaClient()
        if not client.test_connection():
            print("❌ Cannot connect to Ollama!")
            print("💡 Start Ollama: 'ollama serve' or check your URL")
            return
        print("✅ Ollama connected!")
        
        models = client.list_models()
        if models:
            print(f"   Available models: {', '.join(models)}")
        else:
            print("   ⚠️ No models found. Pull one: 'ollama pull llama3.2'")
            return
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return
    
    # Initialize integrated assistant
    print("\n2️⃣ Initializing integrated assistant...")
    try:
        assistant = IntegratedTradingAssistant()
        print("✅ Assistant ready!")
    except Exception as e:
        print(f"❌ Initialization error: {e}")
        return
    
    # Main CLI loop (pattern from app_cli.py)
    while True:
        print("\n" + "=" * 50)
        print("🛠️  OLLAMA TRADING ASSISTANT CLI")
        print("=" * 50)
        print("1. Get AI trading recommendation")
        print("2. Quick recommendation")
        print("3. View market data")
        print("4. View portfolio status")
        print("5. Continuous analysis mode")
        print("6. Exit")
        
        choice = input("\nSelect option [1-6]: ").strip()
        
        if choice == "1":
            print("\n🔍 Analyzing market and generating recommendation...")
            result = assistant.analyze_and_recommend()
            
            print("\n" + "=" * 50)
            print("🤖 AI RECOMMENDATION")
            print("=" * 50)
            rec = result['recommendation']
            print(f"Action: {rec['action']}")
            print(f"Confidence: {rec['confidence']}/10")
            print(f"\nReasoning:\n{result['analysis'][:500]}...")
            print("=" * 50)
            
        elif choice == "2":
            print("\n⚡ Getting quick recommendation...")
            quick_rec = assistant.get_quick_recommendation()
            print(f"\n{quick_rec}")
            
        elif choice == "3":
            print("\n📊 Current Market Data:")
            market_data = assistant.get_live_market_data()
            for key, value in market_data.items():
                print(f"  {key}: {value}")
                
        elif choice == "4":
            print("\n💰 Portfolio Status:")
            portfolio = assistant.get_portfolio_status()
            for key, value in portfolio.items():
                print(f"  {key}: {value}")
                
        elif choice == "5":
            print("\n🔄 Continuous Analysis Mode")
            print("Press Ctrl+C to stop")
            try:
                while True:
                    import time
                    result = assistant.analyze_and_recommend()
                    rec = result['recommendation']
                    print(f"\n[{datetime.now().strftime('%H:%M:%S')}] "
                          f"{rec['action']} (Confidence: {rec['confidence']}/10)")
                    time.sleep(60)  # Analyze every minute
            except KeyboardInterrupt:
                print("\n⏸️  Continuous mode stopped")
                
        elif choice == "6":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please try again.")


def main():
    """Main entry point"""
    try:
        integrated_cli_menu()
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted. Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

