"""
AI-Enhanced Signal Detection
Combines traditional technical analysis with machine learning for adaptive trading signals
"""
import time
import logging
from datetime import datetime, timezone
from typing import Dict, Any, Optional, List, Tuple

# Try to import pandas, fall back to basic implementations
try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False
    print("⚠️ Pandas not available. Using basic implementations.")
from core.drift_client import DriftClient, ETHPerpStrategy
from core.indicators import calculate_rsi, calculate_ema, calculate_bollinger_bands
from app_logger import log_signal
from ai_learning import get_ai_signal, learn_from_trade, TradingSignal, ai_engine

class AISignalDetector:
    """
    AI-enhanced signal detector that combines traditional analysis with machine learning
    """
    
    def __init__(self):
        self.drift_client = DriftClient()
        self.drift_strategy = ETHPerpStrategy(self.drift_client)
        
        # Traditional signal weights (will be adapted by AI)
        self.signal_weights = {
            'rsi': 0.2,
            'ema_cross': 0.15,
            'bollinger': 0.15,
            'funding_rate': 0.1,
            'volume': 0.1,
            'sentiment': 0.1,
            'ai_signal': 0.2  # AI gets significant weight
        }
        
        # Alternative data sources
        self.coingecko_base = "https://api.coingecko.com/api/v3"
        self.binance_base = "https://fapi.binance.com/fapi/v1"
        self.bybit_base = "https://api.bybit.com/v5"
        
        # Signal thresholds (adaptive)
        self.base_threshold = 0.75
        self.current_threshold = self.base_threshold
        
        # Performance tracking for adaptive learning
        self.recent_signals = []
        self.signal_performance = []
        
    def get_market_data(self) -> Dict[str, Any]:
        """Get comprehensive market data for AI analysis"""
        market_data = {}
        
        try:
            # Get current ETH price and basic data
            current_price = self.drift_client.get_current_price()
            market_data['price'] = current_price
            
            # Get technical indicators
            price_history = self.drift_client.get_price_history(period='1h', limit=100)
            if price_history:
                prices = [float(p['close']) for p in price_history]
                
                # Calculate technical indicators
                market_data['rsi'] = calculate_rsi(prices, period=14)
                market_data['ema_12'] = calculate_ema(prices, period=12)
                market_data['ema_26'] = calculate_ema(prices, period=26)
                
                bb_upper, bb_middle, bb_lower = calculate_bollinger_bands(prices, period=20)
                market_data['bb_upper'] = bb_upper
                market_data['bb_middle'] = bb_middle
                market_data['bb_lower'] = bb_lower
                
                # Price changes
                if len(prices) >= 2:
                    market_data['price_change_1h'] = (prices[-1] - prices[-2]) / prices[-2]
                if len(prices) >= 25:
                    market_data['price_change_24h'] = (prices[-1] - prices[-25]) / prices[-25]
            
            # Get funding rate
            funding_rate = self.drift_client.get_funding_rate()
            market_data['funding_rate'] = funding_rate
            
            # Get volume data
            market_data['volume_24h'] = self.drift_client.get_volume_24h()
            
            # Get alternative data
            alt_prices = self.get_alternative_prices()
            alt_funding = self.get_alternative_funding_rates()
            
            # Calculate divergences
            if alt_prices:
                avg_alt_price = sum(alt_prices.values()) / len(alt_prices)
                market_data['price_divergence'] = (current_price - avg_alt_price) / avg_alt_price
            
            if alt_funding:
                avg_alt_funding = sum(alt_funding.values()) / len(alt_funding)
                market_data['funding_divergence'] = funding_rate - avg_alt_funding
            
            # Get sentiment data
            market_data['fear_greed_index'] = self.get_fear_greed_index()
            market_data['social_sentiment'] = self.get_social_sentiment()
            
        except Exception as e:
            logging.warning(f"Error getting market data: {e}")
            # Provide default values
            market_data.update({
                'price': 3000.0,
                'rsi': 50.0,
                'ema_12': 3000.0,
                'ema_26': 3000.0,
                'bb_upper': 3100.0,
                'bb_middle': 3000.0,
                'bb_lower': 2900.0,
                'funding_rate': 0.0,
                'volume_24h': 1000000.0,
                'fear_greed_index': 50.0,
                'social_sentiment': 0.0
            })
        
        return market_data
    
    def get_alternative_prices(self) -> Dict[str, float]:
        """Get ETH prices from alternative sources"""
        import requests
        
        prices = {}
        
        try:
            # CoinGecko ETH price
            cg_resp = requests.get(f"{self.coingecko_base}/simple/price", 
                                 params={'ids': 'ethereum', 'vs_currencies': 'usd'}, timeout=5)
            if cg_resp.status_code == 200:
                data = cg_resp.json()
                prices['coingecko'] = float(data.get('ethereum', {}).get('usd', 0))
        except Exception as e:
            logging.warning(f"Failed to get CoinGecko price: {e}")
            
        try:
            # Binance ETH price
            binance_resp = requests.get(f"{self.binance_base}/ticker/price", 
                                      params={'symbol': 'ETHUSDT'}, timeout=5)
            if binance_resp.status_code == 200:
                data = binance_resp.json()
                prices['binance'] = float(data.get('price', 0))
        except Exception as e:
            logging.warning(f"Failed to get Binance price: {e}")
            
        return prices
    
    def get_alternative_funding_rates(self) -> Dict[str, float]:
        """Get funding rates from alternative exchanges"""
        import requests
        
        funding_rates = {}
        
        try:
            # Binance ETH-USDT perp funding rate
            binance_resp = requests.get(f"{self.binance_base}/premiumIndex", 
                                      params={'symbol': 'ETHUSDT'}, timeout=5)
            if binance_resp.status_code == 200:
                data = binance_resp.json()
                funding_rates['binance'] = float(data.get('lastFundingRate', 0))
        except Exception as e:
            logging.warning(f"Failed to get Binance funding rate: {e}")
            
        return funding_rates
    
    def get_fear_greed_index(self) -> float:
        """Get Fear & Greed Index (simplified)"""
        try:
            import requests
            # Using alternative API since the original requires API key
            response = requests.get("https://api.alternative.me/fng/", timeout=5)
            if response.status_code == 200:
                data = response.json()
                return float(data.get('data', [{}])[0].get('value', 50))
        except:
            pass
        return 50.0  # Neutral
    
    def get_social_sentiment(self) -> float:
        """Get social sentiment (simplified)"""
        # In a real implementation, you'd integrate with social media APIs
        # For now, return a neutral value
        return 0.0
    
    def calculate_traditional_signals(self, market_data: Dict[str, Any]) -> Dict[str, float]:
        """Calculate traditional technical analysis signals"""
        signals = {}
        
        # RSI signal
        rsi = market_data.get('rsi', 50)
        if rsi < 30:
            signals['rsi'] = 0.8  # Strong buy
        elif rsi > 70:
            signals['rsi'] = -0.8  # Strong sell
        elif rsi < 40:
            signals['rsi'] = 0.4  # Weak buy
        elif rsi > 60:
            signals['rsi'] = -0.4  # Weak sell
        else:
            signals['rsi'] = 0.0  # Neutral
        
        # EMA crossover signal
        ema_12 = market_data.get('ema_12', 0)
        ema_26 = market_data.get('ema_26', 0)
        if ema_12 > ema_26:
            signals['ema_cross'] = 0.6  # Bullish
        else:
            signals['ema_cross'] = -0.6  # Bearish
        
        # Bollinger Bands signal
        price = market_data.get('price', 0)
        bb_upper = market_data.get('bb_upper', 0)
        bb_lower = market_data.get('bb_lower', 0)
        bb_middle = market_data.get('bb_middle', 0)
        
        if price < bb_lower:
            signals['bollinger'] = 0.7  # Oversold
        elif price > bb_upper:
            signals['bollinger'] = -0.7  # Overbought
        else:
            signals['bollinger'] = 0.0  # Neutral
        
        # Funding rate signal
        funding_rate = market_data.get('funding_rate', 0)
        if funding_rate > 0.01:
            signals['funding_rate'] = -0.5  # High funding = bearish
        elif funding_rate < -0.01:
            signals['funding_rate'] = 0.5  # Negative funding = bullish
        else:
            signals['funding_rate'] = 0.0
        
        # Volume signal
        volume_24h = market_data.get('volume_24h', 0)
        # Simplified volume analysis
        if volume_24h > 2000000:  # High volume
            signals['volume'] = 0.3
        elif volume_24h < 500000:  # Low volume
            signals['volume'] = -0.3
        else:
            signals['volume'] = 0.0
        
        # Sentiment signal
        fear_greed = market_data.get('fear_greed_index', 50)
        if fear_greed < 25:
            signals['sentiment'] = 0.6  # Extreme fear = buy opportunity
        elif fear_greed > 75:
            signals['sentiment'] = -0.6  # Extreme greed = sell opportunity
        else:
            signals['sentiment'] = 0.0
        
        return signals
    
    def adapt_weights_based_on_performance(self):
        """Adapt signal weights based on recent performance"""
        if len(self.signal_performance) < 10:
            return  # Need more data
        
        # Analyze which signals have been most accurate
        recent_performance = self.signal_performance[-20:]  # Last 20 signals
        
        # Calculate accuracy for each signal type
        signal_accuracy = {}
        for signal_type in self.signal_weights.keys():
            if signal_type == 'ai_signal':
                continue  # Skip AI signal for now
            
            correct_predictions = 0
            total_predictions = 0
            
            for perf in recent_performance:
                if signal_type in perf['signal_scores']:
                    total_predictions += 1
                    if perf['success']:
                        correct_predictions += 1
            
            if total_predictions > 0:
                signal_accuracy[signal_type] = correct_predictions / total_predictions
            else:
                signal_accuracy[signal_type] = 0.5  # Default accuracy
        
        # Adjust weights based on accuracy
        total_weight = sum(self.signal_weights.values()) - self.signal_weights['ai_signal']
        
        for signal_type, accuracy in signal_accuracy.items():
            if signal_type != 'ai_signal':
                # Increase weight for accurate signals, decrease for inaccurate ones
                adjustment_factor = (accuracy - 0.5) * 0.2  # Max 20% adjustment
                new_weight = self.signal_weights[signal_type] * (1 + adjustment_factor)
                self.signal_weights[signal_type] = max(0.05, min(0.4, new_weight))  # Keep within bounds
        
        # Normalize weights
        current_total = sum(self.signal_weights.values()) - self.signal_weights['ai_signal']
        scale_factor = total_weight / current_total if current_total > 0 else 1.0
        
        for signal_type in self.signal_weights.keys():
            if signal_type != 'ai_signal':
                self.signal_weights[signal_type] *= scale_factor
        
        print(f"🔄 Adapted signal weights: {self.signal_weights}")
    
    def generate_ai_enhanced_signal(self, market_data: Dict[str, Any], 
                                  trade_history: List[Dict], 
                                  portfolio_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate AI-enhanced trading signal"""
        
        # Get AI signal
        ai_signal = get_ai_signal(market_data, trade_history, portfolio_data)
        
        # Calculate traditional signals
        traditional_signals = self.calculate_traditional_signals(market_data)
        
        # Combine signals with adaptive weights
        combined_score = 0.0
        signal_details = {}
        
        for signal_type, weight in self.signal_weights.items():
            if signal_type == 'ai_signal':
                # Convert AI signal to score
                if ai_signal.action == 'long':
                    score = ai_signal.confidence
                elif ai_signal.action == 'short':
                    score = -ai_signal.confidence
                else:
                    score = 0.0
                signal_details[signal_type] = score
            else:
                score = traditional_signals.get(signal_type, 0.0)
                signal_details[signal_type] = score
            
            combined_score += score * weight
        
        # Determine final action
        if combined_score > self.current_threshold:
            action = 'long'
            confidence = min(combined_score, 1.0)
        elif combined_score < -self.current_threshold:
            action = 'short'
            confidence = min(abs(combined_score), 1.0)
        else:
            action = 'hold'
            confidence = 0.5
        
        # Create comprehensive signal
        signal_data = {
            'action': action,
            'confidence': confidence,
            'combined_score': combined_score,
            'ai_signal': {
                'action': ai_signal.action,
                'confidence': ai_signal.confidence,
                'reasoning': ai_signal.reasoning
            },
            'traditional_signals': traditional_signals,
            'signal_weights': self.signal_weights.copy(),
            'market_data': market_data,
            'timestamp': datetime.now().isoformat(),
            'model_version': ai_signal.model_version
        }
        
        # Log the signal
        log_signal(f"AI-Enhanced Signal: {action.upper()} (confidence: {confidence:.2f}) - {ai_signal.reasoning}")
        
        # Store for performance tracking
        self.recent_signals.append(signal_data)
        if len(self.recent_signals) > 100:
            self.recent_signals = self.recent_signals[-100:]  # Keep last 100
        
        return signal_data
    
    def update_signal_performance(self, signal_data: Dict[str, Any], trade_outcome: Dict[str, Any]):
        """Update signal performance for adaptive learning"""
        
        success = trade_outcome.get('realized_pnl', 0) > 0
        
        performance_data = {
            'signal_data': signal_data,
            'trade_outcome': trade_outcome,
            'success': success,
            'signal_scores': signal_data.get('traditional_signals', {}),
            'ai_confidence': signal_data.get('ai_signal', {}).get('confidence', 0.0),
            'combined_score': signal_data.get('combined_score', 0.0),
            'timestamp': datetime.now().isoformat()
        }
        
        self.signal_performance.append(performance_data)
        if len(self.signal_performance) > 200:
            self.signal_performance = self.signal_performance[-200:]  # Keep last 200
        
        # Learn from the outcome
        learn_from_trade(
            TradingSignal(
                action=signal_data['action'],
                confidence=signal_data['confidence'],
                features=signal_data.get('market_data', {}),
                timestamp=datetime.fromisoformat(signal_data['timestamp']),
                model_version=signal_data.get('model_version', '1.0.0'),
                reasoning=signal_data.get('ai_signal', {}).get('reasoning', '')
            ),
            trade_outcome
        )
        
        # Adapt weights periodically
        if len(self.signal_performance) % 20 == 0:
            self.adapt_weights_based_on_performance()
    
    def get_signal_statistics(self) -> Dict[str, Any]:
        """Get signal performance statistics"""
        if not self.signal_performance:
            return {'message': 'No performance data available'}
        
        total_signals = len(self.signal_performance)
        successful_signals = sum(1 for p in self.signal_performance if p['success'])
        success_rate = successful_signals / total_signals if total_signals > 0 else 0
        
        # AI signal performance
        ai_signals = [p for p in self.signal_performance if p.get('ai_confidence', 0) > 0.5]
        ai_success_rate = 0
        if ai_signals:
            ai_successful = sum(1 for p in ai_signals if p['success'])
            ai_success_rate = ai_successful / len(ai_signals)
        
        return {
            'total_signals': total_signals,
            'success_rate': success_rate,
            'ai_signals': len(ai_signals),
            'ai_success_rate': ai_success_rate,
            'current_weights': self.signal_weights,
            'current_threshold': self.current_threshold,
            'model_status': ai_engine.get_model_status()
        }

# Global AI signal detector instance
ai_signal_detector = AISignalDetector()

def run_ai_signal_loop(cfg):
    """Run the AI-enhanced signal detection loop"""
    try:
        # Get current market data
        market_data = ai_signal_detector.get_market_data()
        
        # Get trade history and portfolio data
        from core.simulation_engine import simulator
        trade_history = simulator.trade_history
        portfolio_data = simulator.get_portfolio_summary()
        
        # Generate AI-enhanced signal
        signal_data = ai_signal_detector.generate_ai_enhanced_signal(
            market_data, trade_history, portfolio_data
        )
        
        # Return signal in expected format
        return {
            'action': signal_data['action'],
            'confidence': signal_data['confidence'],
            'timestamp': signal_data['timestamp'],
            'ai_enhanced': True,
            'details': signal_data
        }
        
    except Exception as e:
        logging.error(f"Error in AI signal loop: {e}")
        return {
            'action': 'hold',
            'confidence': 0.5,
            'timestamp': datetime.now().isoformat(),
            'ai_enhanced': False,
            'error': str(e)
        }

# Export main functions
__all__ = [
    'AISignalDetector', 'ai_signal_detector', 'run_ai_signal_loop'
]