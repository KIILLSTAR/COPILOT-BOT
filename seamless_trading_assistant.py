#!/usr/bin/env python3
"""
Seamless Trading AI Assistant
Automatically gathers all trading data and provides instant AI recommendations
No clicking, no scanning - everything happens automatically in one go
Uses Ollama cloud services for fast, real-time analysis
"""
import os
import json
import time
from typing import Dict, Any, Optional, List
from datetime import datetime
from threading import Thread, Event

# Import Ollama components
from ollama_client import OllamaClient
from trading_ai_assistant import TradingAIAssistant

# Import configuration
from ai_assistant_config import get_config, is_standalone_mode

# Import Jupiter API (works standalone)
try:
    from core.jupiter_api import JupiterAPI, ETHPerpTrader
    from core.jupiter_integration import JupiterEcosystemAnalyzer
    JUPITER_AVAILABLE = True
except ImportError:
    JUPITER_AVAILABLE = False
    print("⚠️ Jupiter API components unavailable - limited functionality")

# Import existing bot components (optional)
HAS_EXISTING_BOT = False
try:
    from core.price_fetcher import price_fetcher
    from ai_signal_detector import AISignalDetector
    from core.simulation_engine import simulator
    from core.drift_client import DriftClient
    from app_config import trade_config as cfg
    from app_logger import _write_log
    HAS_EXISTING_BOT = True
except ImportError:
    # Bot components not needed for standalone mode
    pass


class SeamlessTradingAssistant:
    """
    Seamless trading assistant that automatically gathers all data
    and provides instant AI recommendations - no manual steps required
    """
    
    def __init__(self, 
                 ollama_url: Optional[str] = None,
                 model_name: Optional[str] = None,
                 enable_comet: Optional[bool] = None,
                 auto_refresh: Optional[int] = None):
        """
        Initialize seamless assistant
        
        Args:
            ollama_url: Ollama cloud URL (if None, uses config or auto-detects)
            model_name: Model to use (if None, uses config)
            enable_comet: Enable Comet ML tracking (if None, uses config)
            auto_refresh: Auto-refresh interval in seconds (if None, uses config)
        """
        # Load configuration
        self.config = get_config()
        self.standalone_mode = is_standalone_mode()
        
        # Use config values or provided overrides
        if ollama_url is None:
            ollama_url = self.config.get('ollama_url')
            if ollama_url is None:
                ollama_url = os.getenv('OLLAMA_URL') or os.getenv('OLLAMA_CLOUD_URL')
        
        if model_name is None:
            model_name = self.config.get('ollama_model', 'llama3.2')
        
        if enable_comet is None:
            enable_comet = self.config.get('comet_enabled', False)
        
        if auto_refresh is None:
            if self.config.get('ai_auto_refresh', False):
                auto_refresh = self.config.get('ai_refresh_interval', 60)
            else:
                auto_refresh = 0
        
        self.ollama_url = ollama_url
        self.model_name = model_name
        self.assistant = TradingAIAssistant(
            ollama_url=ollama_url,
            model_name=model_name,
            enable_comet=enable_comet
        )
        
        # Initialize Jupiter API (PRIMARY - works standalone)
        self.jupiter_api = None
        self.jupiter_eth_trader = None
        self.jupiter_analyzer = None
        
        if JUPITER_AVAILABLE and self.config.get('use_jupiter_perps', True):
            try:
                self.jupiter_api = JupiterAPI()
                self.jupiter_eth_trader = ETHPerpTrader(self.jupiter_api)
                self.jupiter_analyzer = JupiterEcosystemAnalyzer()
                print("✅ Connected to Jupiter API (ETH Perps) - Standalone Mode")
            except Exception as e:
                print(f"⚠️ Jupiter API error: {e}")
        
        # Initialize bot components (only if not standalone and enabled)
        self.signal_detector = None
        self.drift_client = None
        self.use_bot_data = False
        
        if not self.standalone_mode and self.config.get('use_bot_data', False) and HAS_EXISTING_BOT:
            try:
                self.signal_detector = AISignalDetector()
                self.drift_client = DriftClient()
                self.use_bot_data = True
                print("✅ Connected to bot infrastructure (integrated mode)")
            except Exception as e:
                print(f"⚠️ Bot components unavailable: {e}, using standalone mode")
                self.standalone_mode = True
        
        # Auto-refresh functionality
        self.auto_refresh = auto_refresh
        self.auto_refresh_thread = None
        self.stop_event = Event()
        self.last_analysis = None
        self.analysis_callbacks = []
        
    def gather_all_data(self) -> Dict[str, Any]:
        """
        Automatically gather ALL trading data in one go
        No clicking, no manual steps - everything happens automatically
        """
        data = {
            'timestamp': datetime.now().isoformat(),
            'market_data': {},
            'portfolio': {},
            'trade_history': [],
            'positions': [],
            'indicators': {},
            'alternative_data': {}
        }
        
        # 1. Get comprehensive market data from Jupiter (PRIMARY SOURCE)
        # Works standalone - pulls directly from Jupiter API
        if self.jupiter_eth_trader and self.config.get('use_jupiter_perps', True):
            try:
                # Get Jupiter ETH price (primary source - works standalone)
                jupiter_price = self.jupiter_eth_trader.get_eth_price()
                if jupiter_price:
                    data['market_data'] = self._get_jupiter_market_data_standalone(jupiter_price)
                    print("✅ Jupiter market data gathered (ETH Perps) - Standalone")
                else:
                    raise Exception("Jupiter price unavailable")
            except Exception as e:
                print(f"⚠️ Jupiter data error: {e}")
                # Fallback to bot data if available, otherwise basic data
                if self.use_bot_data and self.signal_detector:
                    try:
                        data['market_data'] = self.signal_detector.get_market_data()
                        print("✅ Fallback to bot market data")
                    except:
                        data['market_data'] = self._get_basic_market_data()
                else:
                    data['market_data'] = self._get_basic_market_data()
        elif self.use_bot_data and self.signal_detector:
            # Use bot data if Jupiter not available but bot is enabled
            try:
                data['market_data'] = self.signal_detector.get_market_data()
                print("✅ Bot market data gathered (Jupiter unavailable)")
            except Exception as e:
                print(f"⚠️ Market data error: {e}")
                data['market_data'] = self._get_basic_market_data()
        else:
            # Standalone fallback
            data['market_data'] = self._get_basic_market_data()
        
        # 2. Get portfolio status (only if bot is enabled, not standalone)
        if not self.standalone_mode and self.use_bot_data and HAS_EXISTING_BOT and simulator:
            try:
                portfolio = simulator.get_portfolio_summary()
                data['portfolio'] = {
                    'balance': portfolio.get('balance', 0),
                    'total_pnl': portfolio.get('total_pnl', 0),
                    'realized_pnl': portfolio.get('realized_pnl', 0),
                    'unrealized_pnl': portfolio.get('unrealized_pnl', 0),
                    'open_positions': portfolio.get('open_positions', 0),
                    'total_trades': portfolio.get('total_trades', 0),
                    'win_rate': portfolio.get('win_rate', 0),
                    'roi': portfolio.get('roi', 0),
                    'total_value': portfolio.get('total_value', 0)
                }
                print("✅ Portfolio data gathered")
            except Exception as e:
                print(f"⚠️ Portfolio error: {e}")
        else:
            # Standalone mode - no portfolio data available
            data['portfolio'] = {
                'balance': 0,
                'total_pnl': 0,
                'open_positions': 0,
                'note': 'Standalone mode - no bot portfolio data'
            }
        
        # 3. Get all open positions (only if bot enabled)
        if not self.standalone_mode and self.use_bot_data and HAS_EXISTING_BOT and simulator:
            try:
                positions = []
                for pos_id, position in simulator.positions.items():
                    if hasattr(position, 'unrealized_pnl'):
                        positions.append({
                            'id': pos_id,
                            'symbol': getattr(position, 'symbol', 'ETH'),
                            'side': getattr(position, 'side', 'long'),
                            'entry_price': position.entry_price,
                            'current_price': position.current_price,
                            'size': getattr(position, 'size', 0),
                            'unrealized_pnl': position.unrealized_pnl,
                            'leverage': getattr(position, 'leverage', 1.0)
                        })
                data['positions'] = positions
                print("✅ Positions data gathered")
            except Exception as e:
                print(f"⚠️ Positions error: {e}")
        else:
            # Standalone mode - no positions from bot
            data['positions'] = []
        
        # 4. Get trade history (last 10 trades for context) - only if bot enabled
        if not self.standalone_mode and self.use_bot_data and HAS_EXISTING_BOT and simulator:
            try:
                history = []
                for trade in simulator.trade_history[-10:]:
                    if hasattr(trade, 'realized_pnl'):
                        history.append({
                            'realized_pnl': trade.realized_pnl,
                            'entry_price': trade.entry_price,
                            'exit_price': getattr(trade, 'exit_price', None),
                            'entry_time': trade.entry_time,
                            'exit_time': getattr(trade, 'exit_time', None),
                            'side': getattr(trade, 'side', 'unknown'),
                            'duration_hours': self._calculate_duration(
                                trade.entry_time, 
                                getattr(trade, 'exit_time', None)
                            )
                        })
                data['trade_history'] = history
                print("✅ Trade history gathered")
            except Exception as e:
                print(f"⚠️ Trade history error: {e}")
        else:
            # Standalone mode - no trade history from bot
            data['trade_history'] = []
        
        # 5. Get Jupiter-specific insights (liquidity, volume, sentiment)
        if self.jupiter_analyzer:
            try:
                jupiter_insights = self.jupiter_analyzer.get_jupiter_eth_insights()
                if jupiter_insights:
                    data['jupiter_insights'] = {
                        'eth_price': jupiter_insights.eth_usdc_price,
                        'volume_24h': jupiter_insights.volume_24h,
                        'price_impact': jupiter_insights.price_impact,
                        'route_efficiency': jupiter_insights.route_efficiency,
                        'liquidity_depth': jupiter_insights.liquidity_depth,
                        'swap_count_24h': jupiter_insights.swap_count_24h
                    }
                    
                    # Get Jupiter ecosystem sentiment
                    sentiment = self.jupiter_analyzer.get_eth_ecosystem_sentiment()
                    if sentiment:
                        data['jupiter_insights']['sentiment'] = sentiment.get('sentiment_label', 'neutral')
                        data['jupiter_insights']['sentiment_score'] = sentiment.get('sentiment_score', 0)
                    
                    print("✅ Jupiter insights gathered")
            except Exception as e:
                print(f"⚠️ Jupiter insights error: {e}")
        
        # 6. Get additional indicators (from Jupiter insights if standalone, or bot if integrated)
        if self.jupiter_analyzer:
            # Use Jupiter insights for indicators (works standalone)
            try:
                market_data = data['market_data']
                jupiter_insights = data.get('jupiter_insights', {})
                
                data['indicators'] = {
                    'price_source': 'Jupiter',
                    'volume_trend': 'high' if jupiter_insights.get('volume_24h', 0) > 1000000 else 'low',
                    'liquidity_depth': jupiter_insights.get('liquidity_depth', 0),
                    'route_efficiency': jupiter_insights.get('route_efficiency', 0),
                    'price_impact': jupiter_insights.get('price_impact', 0),
                }
                
                # Add technical indicators from market_data if available
                if 'rsi' in market_data:
                    data['indicators']['rsi'] = market_data.get('rsi', 50)
                    data['indicators']['rsi_signal'] = self._interpret_rsi(market_data.get('rsi', 50))
                if 'ema_12' in market_data:
                    data['indicators']['ema_cross'] = self._check_ema_cross(market_data)
                if 'bb_upper' in market_data:
                    data['indicators']['bollinger_position'] = self._bollinger_position(market_data)
                
                print("✅ Technical indicators gathered (Jupiter-based)")
            except Exception as e:
                print(f"⚠️ Indicators error: {e}")
        elif self.use_bot_data and self.signal_detector:
            # Use bot indicators if available
            try:
                market_data = data['market_data']
                data['indicators'] = {
                    'rsi': market_data.get('rsi', 50),
                    'rsi_signal': self._interpret_rsi(market_data.get('rsi', 50)),
                    'ema_cross': self._check_ema_cross(market_data),
                    'bollinger_position': self._bollinger_position(market_data),
                    'volume_trend': 'high' if market_data.get('volume_24h', 0) > 1000000 else 'low',
                    'funding_rate': market_data.get('funding_rate', 0),
                    'funding_signal': self._interpret_funding(market_data.get('funding_rate', 0))
                }
                print("✅ Technical indicators gathered (bot-based)")
            except Exception as e:
                print(f"⚠️ Indicators error: {e}")
        
        # 7. Get alternative data (sentiment from Jupiter if standalone, or bot if integrated)
        if self.jupiter_analyzer:
            # Jupiter sentiment already in jupiter_insights
            data['alternative_data'] = {
                'jupiter_sentiment': data.get('jupiter_insights', {}).get('sentiment', 'neutral'),
                'jupiter_sentiment_score': data.get('jupiter_insights', {}).get('sentiment_score', 0)
            }
        elif self.use_bot_data and self.signal_detector:
            # Get alternative data from bot if available
            try:
                data['alternative_data'] = {
                    'fear_greed_index': data['market_data'].get('fear_greed_index', 50),
                    'social_sentiment': data['market_data'].get('social_sentiment', 0),
                    'price_divergence': data['market_data'].get('price_divergence', 0)
                }
                print("✅ Alternative data gathered")
            except Exception as e:
                print(f"⚠️ Alternative data error: {e}")
        
        return data
    
    def analyze_and_recommend(self, show_details: bool = True) -> Dict[str, Any]:
        """
        Analyze ALL data and provide recommendation in one seamless operation
        No manual steps - everything happens automatically
        """
        if show_details:
            print("\n🔄 Seamless AI Analysis")
            print("=" * 60)
            print("📊 Gathering all trading data automatically...")
        
        # Gather all data automatically (no clicking, no manual steps)
        all_data = self.gather_all_data()
        
        if show_details:
            print("🤖 AI analyzing complete dataset and generating recommendation...")
        
        # Analyze everything at once
        result = self.assistant.analyze_live_data(
            market_data=all_data['market_data'],
            portfolio=all_data['portfolio'],
            trade_history=all_data['trade_history']
        )
        
        # Add comprehensive context
        result['complete_data'] = all_data
        result['positions'] = all_data['positions']
        result['indicators'] = all_data.get('indicators', {})
        result['alternative_data'] = all_data.get('alternative_data', {})
        
        # Log recommendation (only if bot infrastructure available and enabled)
        if not self.standalone_mode and HAS_EXISTING_BOT:
            try:
                rec = result['recommendation']
                _write_log("SEAMLESS_AI", 
                          f"{rec['action']} | Confidence: {rec['confidence']}/10 | "
                          f"Price: ${all_data['market_data'].get('price', 0):,.2f}")
            except:
                pass
        
        self.last_analysis = result
        
        # Trigger callbacks
        for callback in self.analysis_callbacks:
            try:
                callback(result)
            except Exception as e:
                print(f"⚠️ Callback error: {e}")
        
        return result
    
    def display_analysis(self, result: Optional[Dict[str, Any]] = None):
        """
        Display comprehensive analysis in one clean view
        Everything you need to know in one place
        """
        if result is None:
            result = self.last_analysis
            if result is None:
                print("⚠️ No analysis available. Run analyze_and_recommend() first.")
                return
        
        rec = result['recommendation']
        data = result['complete_data']
        market = data['market_data']
        portfolio = data['portfolio']
        
        print("\n" + "=" * 70)
        print("🤖 SEAMLESS AI TRADING ANALYSIS - JUPITER ETH PERPS")
        print("=" * 70)
        
        # Recommendation
        print(f"\n📊 RECOMMENDATION: {rec['action']}")
        print(f"   Confidence: {rec['confidence']}/10")
        print(f"   Model: {self.model_name}")
        print(f"   Platform: Jupiter ETH Perpetuals")
        print(f"   Timestamp: {result['timestamp']}")
        
        # Jupiter Data Source
        if 'jupiter_insights' in result:
            jupiter = result['jupiter_insights']
            print(f"\n🪐 JUPITER MARKET DATA")
            print(f"   Price: ${jupiter.get('eth_price', market.get('price', 0)):,.2f} (Jupiter)")
            print(f"   24h Volume: ${jupiter.get('volume_24h', 0):,.0f}")
            print(f"   Liquidity Depth: {jupiter.get('liquidity_depth', 0):.2%}")
            print(f"   Price Impact (1 ETH): {jupiter.get('price_impact', 0):.3%}")
            print(f"   Route Efficiency: {jupiter.get('route_efficiency', 0):.2%}")
            if 'sentiment' in jupiter:
                print(f"   Sentiment: {jupiter['sentiment'].upper()} (Score: {jupiter.get('sentiment_score', 0)}/4)")
        
        # Market Summary
        print(f"\n💰 MARKET SUMMARY")
        print(f"   Price: ${market.get('price', 0):,.2f} ({market.get('source', 'Unknown')})")
        if 'indicators' in result:
            ind = result['indicators']
            print(f"   RSI: {market.get('rsi', 50):.1f} ({ind.get('rsi_signal', 'neutral')})")
            print(f"   EMA Cross: {ind.get('ema_cross', 'none')}")
            print(f"   Bollinger: {ind.get('bollinger_position', 'middle')}")
            print(f"   Volume: {ind.get('volume_trend', 'normal')}")
            print(f"   Funding Rate: {market.get('funding_rate', 0):.4f} ({ind.get('funding_signal', 'neutral')})")
        
        # Portfolio Summary
        print(f"\n💼 PORTFOLIO")
        print(f"   Balance: ${portfolio.get('balance', 0):,.2f}")
        print(f"   Total PnL: ${portfolio.get('total_pnl', 0):,.2f}")
        print(f"   Unrealized PnL: ${portfolio.get('unrealized_pnl', 0):,.2f}")
        print(f"   Open Positions: {portfolio.get('open_positions', 0)}")
        print(f"   Win Rate: {portfolio.get('win_rate', 0):.1f}%")
        print(f"   ROI: {portfolio.get('roi', 0):.2f}%")
        
        # Positions
        if result['positions']:
            print(f"\n📈 OPEN POSITIONS")
            for pos in result['positions']:
                pnl_str = f"+${pos['unrealized_pnl']:,.2f}" if pos['unrealized_pnl'] >= 0 else f"-${abs(pos['unrealized_pnl']):,.2f}"
                print(f"   {pos['side'].upper()} {pos['symbol']} @ ${pos['entry_price']:,.2f} | PnL: {pnl_str}")
        
        # AI Reasoning
        print(f"\n🧠 AI REASONING")
        analysis = result.get('analysis', '')
        # Show first 500 chars of analysis
        print(f"   {analysis[:500]}...")
        
        print("=" * 70)
    
    def start_auto_refresh(self):
        """Start automatic refresh of analysis"""
        if self.auto_refresh <= 0:
            print("⚠️ Auto-refresh disabled (set auto_refresh > 0)")
            return
        
        if self.auto_refresh_thread and self.auto_refresh_thread.is_alive():
            print("⚠️ Auto-refresh already running")
            return
        
        self.stop_event.clear()
        
        def refresh_loop():
            while not self.stop_event.is_set():
                try:
                    self.analyze_and_recommend(show_details=False)
                    time.sleep(self.auto_refresh)
                except Exception as e:
                    print(f"⚠️ Auto-refresh error: {e}")
                    time.sleep(5)
        
        self.auto_refresh_thread = Thread(target=refresh_loop, daemon=True)
        self.auto_refresh_thread.start()
        print(f"✅ Auto-refresh started (every {self.auto_refresh} seconds)")
    
    def stop_auto_refresh(self):
        """Stop automatic refresh"""
        if self.auto_refresh_thread:
            self.stop_event.set()
            self.auto_refresh_thread.join(timeout=2)
            print("⏸️  Auto-refresh stopped")
    
    def add_analysis_callback(self, callback):
        """Add callback to be called after each analysis"""
        self.analysis_callbacks.append(callback)
    
    # Helper methods
    def _get_jupiter_market_data_standalone(self, jupiter_price: float) -> Dict[str, Any]:
        """Get comprehensive market data with Jupiter as primary source (works standalone)"""
        market_data = {
            'price': jupiter_price,
            'source': 'Jupiter',
            'platform': 'Jupiter ETH Perps',
            'mode': 'standalone' if self.standalone_mode else 'integrated'
        }
        
        # Try to get additional technical indicators from bot if available (not required)
        if self.use_bot_data and self.signal_detector:
            try:
                full_data = self.signal_detector.get_market_data()
                # Use Jupiter price but keep other indicators
                full_data['price'] = jupiter_price
                full_data['source'] = 'Jupiter'
                full_data['platform'] = 'Jupiter ETH Perps'
                full_data['mode'] = 'integrated'
                return full_data
            except:
                pass
        
        # Standalone Jupiter data (works without bot)
        # Basic structure - Jupiter insights will fill in the rest
        market_data.update({
            'volume_24h': 0,  # Will be filled by Jupiter insights
            'funding_rate': 0.001  # Default, Jupiter doesn't have perps funding directly
        })
        
        return market_data
    
    def _get_basic_market_data(self) -> Dict[str, Any]:
        """Fallback market data (works standalone)"""
        try:
            # Try Jupiter first (works standalone)
            if self.jupiter_eth_trader:
                jupiter_price = self.jupiter_eth_trader.get_eth_price()
                if jupiter_price:
                    return self._get_jupiter_market_data_standalone(jupiter_price)
            
            # Fallback to price fetcher (if bot available)
            if self.use_bot_data and HAS_EXISTING_BOT:
                price = price_fetcher.get_eth_price()
            else:
                price = 3500.0  # Default fallback
        except:
            price = 3500.0
        
        return {
            'price': price,
            'source': 'Fallback',
            'platform': 'Jupiter ETH Perps',
            'mode': 'standalone',
            'volume_24h': 0,
            'funding_rate': 0.001
        }
    
    def _interpret_rsi(self, rsi: float) -> str:
        """Interpret RSI value"""
        if rsi > 70:
            return 'overbought'
        elif rsi < 30:
            return 'oversold'
        else:
            return 'neutral'
    
    def _check_ema_cross(self, market_data: Dict[str, Any]) -> str:
        """Check EMA crossover"""
        ema_12 = market_data.get('ema_12', 0)
        ema_26 = market_data.get('ema_26', 0)
        price = market_data.get('price', 0)
        
        if ema_12 > ema_26:
            return 'bullish' if price > ema_12 else 'weak_bullish'
        else:
            return 'bearish' if price < ema_12 else 'weak_bearish'
    
    def _bollinger_position(self, market_data: Dict[str, Any]) -> str:
        """Check position relative to Bollinger Bands"""
        price = market_data.get('price', 0)
        bb_upper = market_data.get('bb_upper', price)
        bb_lower = market_data.get('bb_lower', price)
        bb_middle = market_data.get('bb_middle', price)
        
        if price >= bb_upper:
            return 'upper_band'
        elif price <= bb_lower:
            return 'lower_band'
        else:
            return 'middle_band'
    
    def _interpret_funding(self, funding_rate: float) -> str:
        """Interpret funding rate"""
        if funding_rate > 0.001:
            return 'positive_long_bias'
        elif funding_rate < -0.001:
            return 'negative_short_bias'
        else:
            return 'neutral'
    
    def _calculate_duration(self, entry_time: str, exit_time: Optional[str]) -> float:
        """Calculate trade duration in hours"""
        try:
            entry = datetime.fromisoformat(entry_time.replace('Z', '+00:00'))
            if exit_time:
                exit = datetime.fromisoformat(exit_time.replace('Z', '+00:00'))
                return (exit - entry).total_seconds() / 3600
            else:
                return (datetime.now() - entry).total_seconds() / 3600
        except:
            return 0.0


def main():
    """Main seamless workflow"""
    print("🚀 Seamless Trading AI Assistant - Jupiter ETH Perps")
    print("=" * 70)
    
    # Configuration - use environment variables or defaults
    ollama_url = os.getenv('OLLAMA_URL') or os.getenv('OLLAMA_CLOUD_URL')
    model_name = os.getenv('OLLAMA_MODEL', 'llama3.2')
    
    if ollama_url:
        print(f"📍 Ollama Cloud: {ollama_url}")
    else:
        print("📍 Using default Ollama configuration")
        print("💡 Set OLLAMA_URL environment variable for cloud service")
    
    print(f"🤖 Model: {model_name}")
    
    # Initialize assistant
    assistant = SeamlessTradingAssistant(
        ollama_url=ollama_url,
        model_name=model_name,
        auto_refresh=0  # Disabled by default
    )
    
    # Test connection
    print("\n🔍 Testing Ollama connection...")
    if not assistant.assistant.ollama.test_connection():
        print("❌ Cannot connect to Ollama!")
        print("💡 Check your OLLAMA_URL environment variable or cloud service")
        return
    print("✅ Connected to Ollama!")
    
    # Main loop
    while True:
        print("\n" + "=" * 70)
        print("🛠️  SEAMLESS TRADING ASSISTANT")
        print("=" * 70)
        print("1. Instant analysis (gathers all data automatically)")
        print("2. Display last analysis")
        print("3. Start auto-refresh (continuous analysis)")
        print("4. Stop auto-refresh")
        print("5. Quick recommendation only")
        print("6. Exit")
        
        choice = input("\nSelect option [1-6]: ").strip()
        
        if choice == "1":
            # Seamless analysis - everything happens automatically
            result = assistant.analyze_and_recommend()
            assistant.display_analysis(result)
            
        elif choice == "2":
            assistant.display_analysis()
            
        elif choice == "3":
            interval = input("Refresh interval (seconds) [default: 60]: ").strip()
            try:
                interval = int(interval) if interval else 60
                assistant.auto_refresh = interval
                assistant.start_auto_refresh()
            except ValueError:
                print("❌ Invalid interval")
                
        elif choice == "4":
            assistant.stop_auto_refresh()
            
        elif choice == "5":
            print("\n⚡ Quick recommendation...")
            quick_rec = assistant.assistant.get_quick_recommendation(
                price=assistant.gather_all_data()['market_data'].get('price', 3500),
                indicators={'rsi': 50, 'ema_trend': 'neutral', 'volume': 'normal'}
            )
            print(f"\n{quick_rec}")
            
        elif choice == "6":
            assistant.stop_auto_refresh()
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted. Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

