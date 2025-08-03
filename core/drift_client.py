"""
Drift Protocol Client for ETH Perpetuals Trading
Provides real perps data including funding rates, mark prices, and positions
"""
import asyncio
import json
import requests
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from datetime import datetime, timezone

@dataclass
class PerpMarketData:
    market_index: int
    symbol: str
    mark_price: float
    index_price: float
    funding_rate: float
    open_interest: float
    base_asset_amount_long: int
    base_asset_amount_short: int
    volume_24h: float
    price_change_24h: float
    
@dataclass
class OrderParams:
    market_type: str  # "perp" or "spot"
    market_index: int
    direction: str    # "long" or "short"
    base_asset_amount: int
    price: Optional[float] = None
    order_type: str = "market"  # "market", "limit", "stop_market", "stop_limit"
    reduce_only: bool = False
    
@dataclass
class Position:
    market_index: int
    base_asset_amount: int
    quote_asset_amount: int
    last_cumulative_funding_rate: int
    last_funding_rate_ts: int
    open_orders: int
    settle_pnl: int
    

class DriftClient:
    """
    Drift Protocol client for ETH perpetuals trading
    """
    
    def __init__(self, rpc_url: str = "https://api.mainnet-beta.solana.com"):
        self.rpc_url = rpc_url
        self.base_url = "https://dlob.drift.trade"
        self.session = requests.Session()
        self.session.headers.update({
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        })
        
        # Market mappings - ETH-PERP is typically market index 2
        self.markets = {
            'ETH-PERP': 2,
            'BTC-PERP': 1,
            'SOL-PERP': 0
        }
    
    def get_eth_perp_data(self) -> Optional[PerpMarketData]:
        """Get comprehensive ETH perpetuals market data"""
        try:
            eth_market_index = self.markets['ETH-PERP']
            response = self.session.get(f"{self.base_url}/markets/perp/{eth_market_index}")
            response.raise_for_status()
            
            data = response.json()
            market = data.get('market', {})
            
            return PerpMarketData(
                market_index=eth_market_index,
                symbol='ETH-PERP',
                mark_price=float(market.get('markPrice', 0)) / 1e6,  # Drift uses 6 decimals
                index_price=float(market.get('indexPrice', 0)) / 1e6,
                funding_rate=float(market.get('fundingRate', 0)) / 1e9,  # 9 decimals for funding
                open_interest=float(market.get('openInterest', 0)) / 1e6,
                base_asset_amount_long=int(market.get('baseAssetAmountLong', 0)),
                base_asset_amount_short=int(market.get('baseAssetAmountShort', 0)),
                volume_24h=float(market.get('volume24h', 0)) / 1e6,
                price_change_24h=float(market.get('priceChange24h', 0))
            )
            
        except Exception as e:
            print(f"[ERROR] Failed to get ETH perp data: {e}")
            return None
    
    def get_funding_rate_history(self, market_index: int = 2, limit: int = 100) -> List[Dict]:
        """Get historical funding rates for ETH-PERP"""
        try:
            response = self.session.get(
                f"{self.base_url}/markets/perp/{market_index}/funding",
                params={'limit': limit}
            )
            response.raise_for_status()
            return response.json().get('fundingRates', [])
            
        except Exception as e:
            print(f"[ERROR] Failed to get funding rate history: {e}")
            return []
    
    def get_orderbook(self, market_index: int = 2, depth: int = 20) -> Dict[str, Any]:
        """Get ETH-PERP orderbook data"""
        try:
            response = self.session.get(
                f"{self.base_url}/orderbook/perp/{market_index}",
                params={'depth': depth}
            )
            response.raise_for_status()
            return response.json()
            
        except Exception as e:
            print(f"[ERROR] Failed to get orderbook: {e}")
            return {}
    
    def get_trades_history(self, market_index: int = 2, limit: int = 100) -> List[Dict]:
        """Get recent trades for ETH-PERP"""
        try:
            response = self.session.get(
                f"{self.base_url}/trades/perp/{market_index}",
                params={'limit': limit}
            )
            response.raise_for_status()
            return response.json().get('trades', [])
            
        except Exception as e:
            print(f"[ERROR] Failed to get trades history: {e}")
            return []
    
    def calculate_funding_payment(self, position_size: float, funding_rate: float) -> float:
        """Calculate funding payment for a position"""
        # Funding payment = position_notional * funding_rate
        # Positive funding rate means longs pay shorts
        return position_size * funding_rate
    
    def get_market_stats(self) -> Dict[str, Any]:
        """Get overall market statistics"""
        try:
            response = self.session.get(f"{self.base_url}/stats")
            response.raise_for_status()
            return response.json()
            
        except Exception as e:
            print(f"[ERROR] Failed to get market stats: {e}")
            return {}
    
    def check_market_conditions(self) -> Dict[str, Any]:
        """
        Analyze current market conditions for trading decisions
        Returns comprehensive market analysis
        """
        eth_data = self.get_eth_perp_data()
        if not eth_data:
            return {}
        
        funding_history = self.get_funding_rate_history(limit=24)  # Last 24 funding periods
        trades = self.get_trades_history(limit=50)
        
        # Calculate funding rate trend
        if len(funding_history) >= 2:
            recent_funding = [float(f.get('fundingRate', 0)) for f in funding_history[:8]]
            avg_recent_funding = sum(recent_funding) / len(recent_funding) if recent_funding else 0
            funding_trend = "increasing" if recent_funding[0] > recent_funding[-1] else "decreasing"
        else:
            avg_recent_funding = eth_data.funding_rate
            funding_trend = "stable"
        
        # Calculate volume trend
        if trades:
            recent_volume = sum(float(t.get('baseAssetAmount', 0)) for t in trades[:10])
            older_volume = sum(float(t.get('baseAssetAmount', 0)) for t in trades[10:20])
            volume_trend = "increasing" if recent_volume > older_volume else "decreasing"
        else:
            volume_trend = "unknown"
        
        # Market skew (long vs short bias)
        total_long = eth_data.base_asset_amount_long
        total_short = abs(eth_data.base_asset_amount_short)
        
        if total_long + total_short > 0:
            long_ratio = total_long / (total_long + total_short)
            if long_ratio > 0.6:
                market_skew = "long_heavy"
            elif long_ratio < 0.4:
                market_skew = "short_heavy"
            else:
                market_skew = "balanced"
        else:
            market_skew = "no_positions"
        
        return {
            'market_data': eth_data,
            'mark_vs_index_spread': eth_data.mark_price - eth_data.index_price,
            'funding_rate_annual': eth_data.funding_rate * 365 * 24,  # Assuming hourly funding
            'avg_recent_funding': avg_recent_funding,
            'funding_trend': funding_trend,
            'volume_trend': volume_trend,
            'market_skew': market_skew,
            'long_ratio': total_long / (total_long + total_short) if (total_long + total_short) > 0 else 0,
            'oi_imbalance': (total_long - total_short) / (total_long + total_short) if (total_long + total_short) > 0 else 0,
            'timestamp': datetime.now(timezone.utc).isoformat()
        }

class ETHPerpStrategy:
    """
    ETH Perpetuals trading strategy using Drift Protocol data
    """
    
    def __init__(self, drift_client: DriftClient):
        self.drift_client = drift_client
        self.min_funding_threshold = 0.01  # 1% annual
        self.max_funding_threshold = 0.10  # 10% annual
        self.volume_spike_threshold = 2.0   # 2x normal volume
        
    def analyze_funding_arbitrage(self) -> Dict[str, Any]:
        """Look for funding rate arbitrage opportunities"""
        conditions = self.drift_client.check_market_conditions()
        
        if not conditions:
            return {'signal': None, 'reason': 'No market data'}
        
        funding_annual = conditions['funding_rate_annual']
        market_skew = conditions['market_skew']
        
        signals = []
        
        # High positive funding - consider shorting (longs pay shorts)
        if funding_annual > self.max_funding_threshold:
            signals.append({
                'direction': 'short',
                'reason': f'High funding rate: {funding_annual:.2%} annually',
                'confidence': min(funding_annual / self.max_funding_threshold, 2.0),
                'strategy': 'funding_arbitrage'
            })
        
        # High negative funding - consider longing (shorts pay longs) 
        elif funding_annual < -self.min_funding_threshold:
            signals.append({
                'direction': 'long', 
                'reason': f'Negative funding rate: {funding_annual:.2%} annually',
                'confidence': min(abs(funding_annual) / self.min_funding_threshold, 2.0),
                'strategy': 'funding_arbitrage'
            })
        
        # Market skew analysis
        if market_skew == 'long_heavy' and funding_annual > 0:
            signals.append({
                'direction': 'short',
                'reason': 'Long-heavy market with positive funding',
                'confidence': 1.2,
                'strategy': 'contrarian_skew'
            })
        elif market_skew == 'short_heavy' and funding_annual < 0:
            signals.append({
                'direction': 'long',
                'reason': 'Short-heavy market with negative funding', 
                'confidence': 1.2,
                'strategy': 'contrarian_skew'
            })
        
        return {
            'signals': signals,
            'market_conditions': conditions,
            'timestamp': datetime.now(timezone.utc).isoformat()
        }
    
    def analyze_momentum(self) -> Dict[str, Any]:
        """Analyze price momentum and volume"""
        eth_data = self.drift_client.get_eth_perp_data()
        if not eth_data:
            return {'signal': None, 'reason': 'No market data'}
        
        trades = self.drift_client.get_trades_history(limit=100)
        if not trades:
            return {'signal': None, 'reason': 'No trade data'}
        
        # Price momentum
        price_change = eth_data.price_change_24h
        
        # Volume analysis
        recent_trades = trades[:20]
        older_trades = trades[20:40] if len(trades) > 40 else trades[20:]
        
        recent_volume = sum(float(t.get('baseAssetAmount', 0)) for t in recent_trades)
        older_volume = sum(float(t.get('baseAssetAmount', 0)) for t in older_trades) if older_trades else recent_volume
        
        volume_ratio = recent_volume / older_volume if older_volume > 0 else 1
        
        signals = []
        
        # Strong momentum with volume confirmation
        if price_change > 0.02 and volume_ratio > self.volume_spike_threshold:  # 2% price + volume spike
            signals.append({
                'direction': 'long',
                'reason': f'Strong upward momentum {price_change:.2%} with volume spike {volume_ratio:.1f}x',
                'confidence': min(price_change * 10 + volume_ratio * 0.5, 3.0),
                'strategy': 'momentum'
            })
        elif price_change < -0.02 and volume_ratio > self.volume_spike_threshold:  # -2% price + volume spike
            signals.append({
                'direction': 'short',
                'reason': f'Strong downward momentum {price_change:.2%} with volume spike {volume_ratio:.1f}x',
                'confidence': min(abs(price_change) * 10 + volume_ratio * 0.5, 3.0),
                'strategy': 'momentum'
            })
        
        return {
            'signals': signals,
            'price_change_24h': price_change,
            'volume_ratio': volume_ratio,
            'mark_price': eth_data.mark_price,
            'timestamp': datetime.now(timezone.utc).isoformat()
        }

# Example usage and testing
if __name__ == "__main__":
    drift_client = DriftClient()
    strategy = ETHPerpStrategy(drift_client)
    
    print("=== ETH Perpetuals Market Data ===")
    eth_data = drift_client.get_eth_perp_data()
    if eth_data:
        print(f"Mark Price: ${eth_data.mark_price:,.2f}")
        print(f"Index Price: ${eth_data.index_price:,.2f}")
        print(f"Funding Rate: {eth_data.funding_rate:.6f} ({eth_data.funding_rate * 365 * 24:.2%} annual)")
        print(f"Open Interest: ${eth_data.open_interest:,.0f}")
        print(f"24h Volume: ${eth_data.volume_24h:,.0f}")
        print(f"24h Change: {eth_data.price_change_24h:.2%}")
    
    print("\n=== Market Analysis ===")
    conditions = drift_client.check_market_conditions()
    if conditions:
        print(f"Market Skew: {conditions['market_skew']}")
        print(f"Long Ratio: {conditions['long_ratio']:.1%}")
        print(f"Funding Trend: {conditions['funding_trend']}")
    
    print("\n=== Trading Signals ===")
    funding_signals = strategy.analyze_funding_arbitrage()
    momentum_signals = strategy.analyze_momentum()
    
    for signal_type, analysis in [('Funding', funding_signals), ('Momentum', momentum_signals)]:
        if analysis.get('signals'):
            print(f"\n{signal_type} Signals:")
            for signal in analysis['signals']:
                print(f"  {signal['direction'].upper()}: {signal['reason']} (Confidence: {signal['confidence']:.1f})")
