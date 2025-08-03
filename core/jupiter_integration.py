"""
Jupiter Integration Module
Provides complementary market data to enhance Drift ETH perps trading
Uses Jupiter's spot data, volume metrics, and ecosystem insights
"""
import requests
import json
from typing import Dict, Any, Optional, List
from datetime import datetime, timezone
from dataclasses import dataclass
from core.jupiter_api import JupiterAPI, ETHPerpTrader

@dataclass
class JupiterMarketInsights:
    eth_usdc_price: float
    volume_24h: float
    price_impact: float
    route_efficiency: float
    liquidity_depth: float
    swap_count_24h: int
    timestamp: str

class JupiterEcosystemAnalyzer:
    """
    Analyzes Jupiter ecosystem data to complement Drift perps trading
    """
    
    def __init__(self):
        self.jupiter_api = JupiterAPI()
        self.eth_trader = ETHPerpTrader(self.jupiter_api)
        
        # Jupiter-specific endpoints for analytics
        self.jupiter_stats_url = "https://stats.jup.ag/coingecko"
        self.volume_url = "https://cache.jup.ag/stats"
        
        # Token addresses for ETH on Solana (Wormhole wrapped)
        self.eth_mint = "7vfCXTUXx5WJV5JADk17DUJ4ksgau7utNKj4b963voxs"
        self.usdc_mint = "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"
    
    def get_jupiter_eth_insights(self) -> Optional[JupiterMarketInsights]:
        """Get comprehensive ETH trading insights from Jupiter"""
        try:
            # Get current ETH price through Jupiter
            eth_price = self.eth_trader.get_eth_price()
            if not eth_price:
                return None
            
            # Get volume and activity data
            volume_data = self._get_volume_metrics()
            liquidity_data = self._get_liquidity_metrics()
            
            return JupiterMarketInsights(
                eth_usdc_price=eth_price,
                volume_24h=volume_data.get('eth_volume_24h', 0),
                price_impact=liquidity_data.get('price_impact_1_eth', 0),
                route_efficiency=liquidity_data.get('route_efficiency', 0),
                liquidity_depth=liquidity_data.get('liquidity_depth', 0),
                swap_count_24h=volume_data.get('swap_count_24h', 0),
                timestamp=datetime.now(timezone.utc).isoformat()
            )
            
        except Exception as e:
            print(f"[ERROR] Failed to get Jupiter ETH insights: {e}")
            return None
    
    def _get_volume_metrics(self) -> Dict[str, Any]:
        """Get volume and trading activity metrics from Jupiter"""
        try:
            response = requests.get(self.volume_url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                
                # Extract ETH-related volume data
                return {
                    'eth_volume_24h': self._extract_eth_volume(data),
                    'swap_count_24h': data.get('24h_volume', {}).get('swapCount', 0),
                    'total_volume_24h': data.get('24h_volume', {}).get('volume', 0)
                }
        except Exception as e:
            print(f"[WARNING] Failed to get Jupiter volume metrics: {e}")
        
        return {}
    
    def _get_liquidity_metrics(self) -> Dict[str, Any]:
        """Analyze ETH liquidity on Jupiter by testing quotes"""
        try:
            # Test various trade sizes to assess liquidity depth
            test_amounts = [0.1, 0.5, 1.0, 5.0, 10.0]  # ETH amounts
            price_impacts = []
            
            base_quote = self.jupiter_api.get_quote(
                self.jupiter_api.QuoteRequest(
                    input_mint=self.eth_mint,
                    output_mint=self.usdc_mint,
                    amount=int(0.1 * 1e8),  # 0.1 ETH
                    slippage_bps=50
                )
            )
            
            if not base_quote:
                return {}
            
            base_price = int(base_quote['outAmount']) / int(base_quote['inAmount'])
            
            # Test price impact for different sizes
            for amount in test_amounts:
                quote = self.jupiter_api.get_quote(
                    self.jupiter_api.QuoteRequest(
                        input_mint=self.eth_mint,
                        output_mint=self.usdc_mint,
                        amount=int(amount * 1e8),
                        slippage_bps=50
                    )
                )
                
                if quote:
                    trade_price = int(quote['outAmount']) / int(quote['inAmount'])
                    price_impact = abs(trade_price - base_price) / base_price
                    price_impacts.append(price_impact)
            
            # Calculate liquidity metrics
            avg_price_impact = sum(price_impacts) / len(price_impacts) if price_impacts else 0
            max_price_impact = max(price_impacts) if price_impacts else 0
            
            return {
                'price_impact_1_eth': price_impacts[2] if len(price_impacts) > 2 else 0,
                'avg_price_impact': avg_price_impact,
                'max_price_impact': max_price_impact,
                'route_efficiency': 1 - avg_price_impact,  # Higher is better
                'liquidity_depth': self._calculate_liquidity_depth(price_impacts, test_amounts)
            }
            
        except Exception as e:
            print(f"[WARNING] Failed to get Jupiter liquidity metrics: {e}")
            return {}
    
    def _extract_eth_volume(self, volume_data: Dict) -> float:
        """Extract ETH-specific volume from Jupiter stats"""
        try:
            # Look for ETH in the top tokens by volume
            top_tokens = volume_data.get('24h_volume', {}).get('topTokens', [])
            
            for token in top_tokens:
                if token.get('mint') == self.eth_mint:
                    return float(token.get('volume', 0))
            
            # Fallback: estimate based on total volume
            total_volume = float(volume_data.get('24h_volume', {}).get('volume', 0))
            return total_volume * 0.05  # Assume ETH is ~5% of total volume
            
        except Exception:
            return 0
    
    def _calculate_liquidity_depth(self, price_impacts: List[float], amounts: List[float]) -> float:
        """Calculate a liquidity depth score"""
        if not price_impacts or not amounts:
            return 0
        
        # Score based on how well Jupiter handles larger trades
        large_trade_impact = price_impacts[-1] if len(price_impacts) > 0 else 1
        
        # Lower price impact for large trades = higher liquidity depth
        return max(0, 1 - large_trade_impact * 10)  # Scale factor for interpretation
    
    def compare_with_drift_pricing(self, drift_mark_price: float) -> Dict[str, Any]:
        """Compare Jupiter spot pricing with Drift mark price"""
        jupiter_insights = self.get_jupiter_eth_insights()
        
        if not jupiter_insights:
            return {'error': 'No Jupiter data available'}
        
        jupiter_price = jupiter_insights.eth_usdc_price
        price_difference = (drift_mark_price - jupiter_price) / jupiter_price
        
        # Analyze the price divergence
        analysis = {
            'jupiter_spot_price': jupiter_price,
            'drift_mark_price': drift_mark_price,
            'price_difference_pct': price_difference * 100,
            'absolute_difference': abs(price_difference),
            'drift_premium_discount': 'premium' if price_difference > 0 else 'discount',
            'arbitrage_opportunity': abs(price_difference) > 0.002,  # 0.2% threshold
            'jupiter_insights': jupiter_insights
        }
        
        # Add market interpretation
        if abs(price_difference) > 0.005:  # 0.5% threshold
            if price_difference > 0:
                analysis['market_interpretation'] = 'Drift trading at premium - potential short opportunity'
            else:
                analysis['market_interpretation'] = 'Drift trading at discount - potential long opportunity'
        else:
            analysis['market_interpretation'] = 'Prices well-aligned - no significant arbitrage'
        
        return analysis
    
    def get_eth_ecosystem_sentiment(self) -> Dict[str, Any]:
        """Analyze ETH ecosystem sentiment through Jupiter activity"""
        try:
            insights = self.get_jupiter_eth_insights()
            if not insights:
                return {}
            
            # Analyze trading patterns
            volume_24h = insights.volume_24h
            swap_count = insights.swap_count_24h
            avg_trade_size = volume_24h / swap_count if swap_count > 0 else 0
            
            # Sentiment indicators
            sentiment_score = 0
            sentiment_factors = []
            
            # High volume indicates interest
            if volume_24h > 1000000:  # $1M+ daily volume
                sentiment_score += 1
                sentiment_factors.append("High trading volume indicates strong interest")
            
            # Large average trade size indicates institutional activity
            if avg_trade_size > 10000:  # $10k+ average trade
                sentiment_score += 1
                sentiment_factors.append("Large average trade size suggests institutional participation")
            
            # Low price impact indicates good liquidity
            if insights.price_impact < 0.01:  # <1% price impact for 1 ETH
                sentiment_score += 1
                sentiment_factors.append("Low price impact indicates healthy liquidity")
            
            # High route efficiency indicates competitive market
            if insights.route_efficiency > 0.98:  # >98% efficiency
                sentiment_score += 1
                sentiment_factors.append("High route efficiency indicates competitive pricing")
            
            sentiment_label = 'bearish'
            if sentiment_score >= 3:
                sentiment_label = 'bullish'
            elif sentiment_score >= 2:
                sentiment_label = 'neutral'
            
            return {
                'sentiment_score': sentiment_score,
                'sentiment_label': sentiment_label,
                'sentiment_factors': sentiment_factors,
                'volume_24h': volume_24h,
                'avg_trade_size': avg_trade_size,
                'swap_count_24h': swap_count,
                'price_impact_1eth': insights.price_impact,
                'route_efficiency': insights.route_efficiency,
                'timestamp': datetime.now(timezone.utc).isoformat()
            }
            
        except Exception as e:
            print(f"[ERROR] Failed to analyze ETH ecosystem sentiment: {e}")
            return {}

class JupiterDriftArbitrageDetector:
    """
    Detects arbitrage opportunities between Jupiter spot and Drift perps
    """
    
    def __init__(self):
        self.jupiter_analyzer = JupiterEcosystemAnalyzer()
        self.min_arbitrage_threshold = 0.002  # 0.2%
        self.min_volume_threshold = 50000     # $50k minimum volume
    
    def detect_arbitrage_opportunities(self, drift_market_data: Dict) -> Dict[str, Any]:
        """
        Detect arbitrage opportunities between Jupiter and Drift
        """
        try:
            drift_mark_price = drift_market_data.get('mark_price', 0)
            drift_index_price = drift_market_data.get('index_price', 0)
            
            if not drift_mark_price:
                return {'error': 'No Drift market data'}
            
            # Compare with Jupiter pricing
            jupiter_comparison = self.jupiter_analyzer.compare_with_drift_pricing(drift_mark_price)
            
            if 'error' in jupiter_comparison:
                return jupiter_comparison
            
            # Get ecosystem sentiment
            ecosystem_sentiment = self.jupiter_analyzer.get_eth_ecosystem_sentiment()
            
            opportunities = []
            
            # Check for mark/index arbitrage on Drift
            mark_index_diff = abs(drift_mark_price - drift_index_price) / drift_index_price
            if mark_index_diff > 0.001:  # 0.1% threshold
                opportunities.append({
                    'type': 'mark_index_arbitrage',
                    'description': f'Drift mark price {mark_index_diff:.3%} away from index',
                    'opportunity_size': mark_index_diff,
                    'confidence': min(mark_index_diff / 0.001, 3.0)
                })
            
            # Check for Jupiter-Drift arbitrage
            if jupiter_comparison.get('arbitrage_opportunity'):
                price_diff = jupiter_comparison.get('absolute_difference', 0)
                opportunities.append({
                    'type': 'jupiter_drift_arbitrage',
                    'description': f'Price difference: {price_diff:.3%} between Jupiter spot and Drift mark',
                    'opportunity_size': price_diff,
                    'confidence': min(price_diff / self.min_arbitrage_threshold, 2.5),
                    'direction': 'buy_drift_sell_jupiter' if jupiter_comparison.get('price_difference_pct', 0) < 0 else 'sell_drift_buy_jupiter'
                })
            
            # Filter opportunities by minimum thresholds
            significant_opportunities = [
                opp for opp in opportunities 
                if opp['opportunity_size'] > self.min_arbitrage_threshold and
                   opp['confidence'] > 1.0
            ]
            
            return {
                'opportunities': significant_opportunities,
                'jupiter_comparison': jupiter_comparison,
                'ecosystem_sentiment': ecosystem_sentiment,
                'market_conditions': {
                    'drift_mark_price': drift_mark_price,
                    'drift_index_price': drift_index_price,
                    'jupiter_spot_price': jupiter_comparison.get('jupiter_spot_price'),
                    'mark_index_spread': mark_index_diff,
                    'jupiter_drift_spread': jupiter_comparison.get('absolute_difference', 0)
                },
                'timestamp': datetime.now(timezone.utc).isoformat()
            }
            
        except Exception as e:
            print(f"[ERROR] Arbitrage detection failed: {e}")
            return {'error': str(e)}
    
    def generate_arbitrage_signals(self, arbitrage_data: Dict) -> List[Dict[str, Any]]:
        """
        Generate trading signals based on arbitrage opportunities
        """
        signals = []
        opportunities = arbitrage_data.get('opportunities', [])
        ecosystem_sentiment = arbitrage_data.get('ecosystem_sentiment', {})
        
        for opp in opportunities:
            if opp['confidence'] > 1.5:  # High confidence threshold
                
                if opp['type'] == 'jupiter_drift_arbitrage':
                    direction = 'long' if 'buy_drift' in opp.get('direction', '') else 'short'
                    signals.append({
                        'direction': direction,
                        'reason': f"Jupiter-Drift arbitrage: {opp['description']}",
                        'confidence': opp['confidence'],
                        'strategy': 'cross_platform_arbitrage',
                        'opportunity_size': opp['opportunity_size']
                    })
                
                elif opp['type'] == 'mark_index_arbitrage':
                    # Mark trading above index suggests long pressure
                    market_conditions = arbitrage_data.get('market_conditions', {})
                    drift_mark = market_conditions.get('drift_mark_price', 0)
                    drift_index = market_conditions.get('drift_index_price', 0)
                    
                    if drift_mark > drift_index:
                        direction = 'short'  # Mark premium suggests potential reversal
                        reason = "Drift mark trading at premium to index - potential short"
                    else:
                        direction = 'long'   # Mark discount suggests potential recovery
                        reason = "Drift mark trading at discount to index - potential long"
                    
                    signals.append({
                        'direction': direction,
                        'reason': reason,
                        'confidence': opp['confidence'],
                        'strategy': 'mark_index_arbitrage',
                        'opportunity_size': opp['opportunity_size']
                    })
        
        # Add ecosystem sentiment-based signals
        sentiment = ecosystem_sentiment.get('sentiment_label', 'neutral')
        sentiment_score = ecosystem_sentiment.get('sentiment_score', 0)
        
        if sentiment == 'bullish' and sentiment_score >= 3:
            signals.append({
                'direction': 'long',
                'reason': f"Strong Jupiter ecosystem sentiment (score: {sentiment_score}/4)",
                'confidence': 1.2 + (sentiment_score * 0.2),
                'strategy': 'ecosystem_sentiment'
            })
        elif sentiment == 'bearish' and sentiment_score <= 1:
            signals.append({
                'direction': 'short',
                'reason': f"Weak Jupiter ecosystem sentiment (score: {sentiment_score}/4)",
                'confidence': 1.2 + ((4 - sentiment_score) * 0.2),
                'strategy': 'ecosystem_sentiment'
            })
        
        return signals

# Example usage and testing
if __name__ == "__main__":
    jupiter_analyzer = JupiterEcosystemAnalyzer()
    arbitrage_detector = JupiterDriftArbitrageDetector()
    
    print("=== Jupiter ETH Ecosystem Analysis ===")
    insights = jupiter_analyzer.get_jupiter_eth_insights()
    if insights:
        print(f"ETH Price: ${insights.eth_usdc_price:.2f}")
        print(f"24h Volume: ${insights.volume_24h:,.0f}")
        print(f"Price Impact (1 ETH): {insights.price_impact:.3%}")
        print(f"Route Efficiency: {insights.route_efficiency:.2%}")
        print(f"24h Swaps: {insights.swap_count_24h:,}")
    
    print("\n=== Ecosystem Sentiment ===")
    sentiment = jupiter_analyzer.get_eth_ecosystem_sentiment()
    if sentiment:
        print(f"Sentiment: {sentiment.get('sentiment_label', 'unknown').upper()}")
        print(f"Score: {sentiment.get('sentiment_score', 0)}/4")
        for factor in sentiment.get('sentiment_factors', []):
            print(f"  • {factor}")
    
    # Test arbitrage detection with sample Drift data
    sample_drift_data = {
        'mark_price': 3520.50,
        'index_price': 3518.75,
        'funding_rate': 0.0001
    }
    
    print("\n=== Arbitrage Opportunities ===")
    arbitrage_result = arbitrage_detector.detect_arbitrage_opportunities(sample_drift_data)
    if arbitrage_result.get('opportunities'):
        for opp in arbitrage_result['opportunities']:
            print(f"  {opp['type']}: {opp['description']} (confidence: {opp['confidence']:.1f})")
    else:
        print("  No significant arbitrage opportunities detected")
    
    print("\n=== Generated Signals ===")
    signals = arbitrage_detector.generate_arbitrage_signals(arbitrage_result)
    for signal in signals:
        print(f"  {signal['direction'].upper()}: {signal['reason']} (confidence: {signal['confidence']:.1f})")