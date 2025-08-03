"""
Enhanced Signal Detection for ETH Perpetuals Trading
Integrates Drift Protocol with alternative data sources for robust trading signals
"""
import time
import logging
import pandas as pd
from datetime import datetime, timezone
from typing import Dict, Any, Optional, List, Tuple
from core.drift_client import DriftClient, ETHPerpStrategy
from core.indicators import calculate_rsi, calculate_ema, calculate_bollinger_bands
from logger.audit_logger import log_signal

class MultiSourceETHPerpAnalyzer:
    """
    Combines Drift Protocol ETH perps with alternative data sources
    """
    
    def __init__(self):
        self.drift_client = DriftClient()
        self.drift_strategy = ETHPerpStrategy(self.drift_client)
        
        # Alternative data sources
        self.coingecko_base = "https://api.coingecko.com/api/v3"
        self.binance_base = "https://fapi.binance.com/fapi/v1"
        self.bybit_base = "https://api.bybit.com/v5"
        
        # Signal thresholds
        self.funding_divergence_threshold = 0.05  # 5% difference between exchanges
        self.price_divergence_threshold = 0.002   # 0.2% price difference
        
    def get_alternative_funding_rates(self) -> Dict[str, float]:
        """Get funding rates from alternative exchanges for comparison"""
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
            
        try:
            # Bybit ETH-USDT perp funding rate
            bybit_resp = requests.get(f"{self.bybit_base}/market/tickers", 
                                    params={'category': 'linear', 'symbol': 'ETHUSDT'}, timeout=5)
            if bybit_resp.status_code == 200:
                data = bybit_resp.json()
                result = data.get('result', {}).get('list', [])
                if result:
                    funding_rates['bybit'] = float(result[0].get('fundingRate', 0))
        except Exception as e:
            logging.warning(f"Failed to get Bybit funding rate: {e}")
            
        return funding_rates
    
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
    
    def get_defi_pulse_data(self) -> Dict[str, Any]:
        """Get DeFi metrics that can affect ETH price"""
        import requests
        
        try:
            # Alternative: Use DeFiLlama TVL data
            defillama_resp = requests.get("https://api.llama.fi/protocols", timeout=10)
            if defillama_resp.status_code == 200:
                protocols = defillama_resp.json()
                eth_tvl = sum(p.get('tvl', 0) for p in protocols if 'ethereum' in p.get('chains', []))
                return {
                    'total_eth_tvl': eth_tvl,
                    'timestamp': datetime.now(timezone.utc).isoformat()
                }
        except Exception as e:
            logging.warning(f"Failed to get DeFi data: {e}")
            
        return {}
    
    def analyze_cross_exchange_arbitrage(self) -> Dict[str, Any]:
        """Analyze funding rate and price differences across exchanges"""
        # Get Drift data
        drift_conditions = self.drift_client.check_market_conditions()
        if not drift_conditions:
            return {'signal': None, 'reason': 'No Drift data available'}
        
        drift_funding = drift_conditions.get('funding_rate_annual', 0)
        drift_price = drift_conditions.get('market_data', {})
        
        if not drift_price:
            return {'signal': None, 'reason': 'No Drift price data'}
        
        # Get alternative data
        alt_funding = self.get_alternative_funding_rates()
        alt_prices = self.get_alternative_prices()
        
        signals = []
        arbitrage_opportunities = []
        
        # Funding rate arbitrage analysis
        for exchange, funding_rate in alt_funding.items():
            funding_diff = drift_funding - (funding_rate * 365 * 24)  # Convert to annual
            
            if abs(funding_diff) > self.funding_divergence_threshold:
                direction = 'long_drift_short_alt' if funding_diff > 0 else 'short_drift_long_alt'
                arbitrage_opportunities.append({
                    'type': 'funding_arbitrage',
                    'exchange': exchange,
                    'drift_funding': drift_funding,
                    'alt_funding': funding_rate * 365 * 24,
                    'difference': funding_diff,
                    'direction': direction,
                    'confidence': min(abs(funding_diff) / self.funding_divergence_threshold, 3.0)
                })
        
        # Price arbitrage analysis
        drift_mark_price = drift_price.mark_price
        for exchange, price in alt_prices.items():
            price_diff = (drift_mark_price - price) / price
            
            if abs(price_diff) > self.price_divergence_threshold:
                direction = 'buy_drift_sell_alt' if price_diff < 0 else 'sell_drift_buy_alt'
                arbitrage_opportunities.append({
                    'type': 'price_arbitrage',
                    'exchange': exchange,
                    'drift_price': drift_mark_price,
                    'alt_price': price,
                    'difference_pct': price_diff,
                    'direction': direction,
                    'confidence': min(abs(price_diff) / self.price_divergence_threshold, 2.0)
                })
        
        # Generate trading signals based on arbitrage opportunities
        for opp in arbitrage_opportunities:
            if opp['confidence'] > 1.5:  # High confidence threshold
                if opp['type'] == 'funding_arbitrage':
                    if 'long_drift' in opp['direction']:
                        signals.append({
                            'direction': 'long',
                            'reason': f"Funding arbitrage vs {opp['exchange']}: Drift {opp['drift_funding']:.2%} vs {opp['alt_funding']:.2%}",
                            'confidence': opp['confidence'],
                            'strategy': 'cross_exchange_funding'
                        })
                    else:
                        signals.append({
                            'direction': 'short',
                            'reason': f"Funding arbitrage vs {opp['exchange']}: Drift {opp['drift_funding']:.2%} vs {opp['alt_funding']:.2%}",
                            'confidence': opp['confidence'],
                            'strategy': 'cross_exchange_funding'
                        })
                
                elif opp['type'] == 'price_arbitrage':
                    if 'buy_drift' in opp['direction']:
                        signals.append({
                            'direction': 'long',
                            'reason': f"Price arbitrage vs {opp['exchange']}: Drift ${opp['drift_price']:.2f} vs ${opp['alt_price']:.2f}",
                            'confidence': opp['confidence'],
                            'strategy': 'cross_exchange_price'
                        })
        
        return {
            'signals': signals,
            'arbitrage_opportunities': arbitrage_opportunities,
            'drift_data': drift_conditions,
            'alternative_funding': alt_funding,
            'alternative_prices': alt_prices,
            'timestamp': datetime.now(timezone.utc).isoformat()
        }

class EnhancedETHPerpSignalDetector:
    """
    Enhanced signal detector combining multiple strategies and data sources
    """
    
    def __init__(self):
        self.multi_source_analyzer = MultiSourceETHPerpAnalyzer()
        self.drift_client = self.multi_source_analyzer.drift_client
        self.drift_strategy = self.multi_source_analyzer.drift_strategy
        
        # Technical analysis parameters
        self.rsi_period = 14
        self.ema_short = 9
        self.ema_long = 21
        self.bollinger_period = 20
        
        # Signal aggregation weights
        self.strategy_weights = {
            'funding_arbitrage': 2.0,
            'cross_exchange_funding': 1.5,
            'momentum': 1.2,
            'technical': 1.0,
            'contrarian_skew': 0.8
        }
        
    def get_price_history(self, limit: int = 100) -> List[float]:
        """Get historical price data from Drift trades"""
        trades = self.drift_client.get_trades_history(limit=limit)
        prices = []
        
        for trade in trades:
            # Calculate trade price from base and quote amounts
            base_amount = float(trade.get('baseAssetAmount', 0))
            quote_amount = float(trade.get('quoteAssetAmount', 0))
            
            if base_amount != 0:
                price = abs(quote_amount) / abs(base_amount) / 1e6  # Adjust for decimals
                prices.append(price)
        
        return prices[::-1]  # Reverse to get chronological order
    
    def calculate_technical_indicators(self) -> Dict[str, Any]:
        """Calculate technical indicators from price history"""
        prices = self.get_price_history(100)
        
        if len(prices) < self.bollinger_period:
            return {}
        
        df = pd.DataFrame({'price': prices})
        
        # Calculate indicators
        rsi = calculate_rsi(df['price'], self.rsi_period)
        ema_short = calculate_ema(df['price'], self.ema_short)
        ema_long = calculate_ema(df['price'], self.ema_long)
        bb_upper, bb_middle, bb_lower = calculate_bollinger_bands(df['price'], self.bollinger_period)
        
        current_price = prices[-1]
        current_rsi = rsi.iloc[-1] if len(rsi) > 0 else 50
        current_ema_short = ema_short.iloc[-1] if len(ema_short) > 0 else current_price
        current_ema_long = ema_long.iloc[-1] if len(ema_long) > 0 else current_price
        current_bb_upper = bb_upper.iloc[-1] if len(bb_upper) > 0 else current_price
        current_bb_lower = bb_lower.iloc[-1] if len(bb_lower) > 0 else current_price
        
        return {
            'rsi': current_rsi,
            'ema_short': current_ema_short,
            'ema_long': current_ema_long,
            'bb_upper': current_bb_upper,
            'bb_lower': current_bb_lower,
            'current_price': current_price,
            'ema_crossover': current_ema_short > current_ema_long,
            'bb_position': 'upper' if current_price > current_bb_upper else 'lower' if current_price < current_bb_lower else 'middle'
        }
    
    def generate_technical_signals(self, indicators: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate signals based on technical indicators"""
        signals = []
        
        if not indicators:
            return signals
        
        rsi = indicators['rsi']
        ema_crossover = indicators['ema_crossover']
        bb_position = indicators['bb_position']
        
        # RSI signals
        if rsi < 30:
            signals.append({
                'direction': 'long',
                'reason': f'RSI oversold: {rsi:.1f}',
                'confidence': min((30 - rsi) / 10, 2.0),
                'strategy': 'technical'
            })
        elif rsi > 70:
            signals.append({
                'direction': 'short',
                'reason': f'RSI overbought: {rsi:.1f}',
                'confidence': min((rsi - 70) / 10, 2.0),
                'strategy': 'technical'
            })
        
        # EMA crossover signals
        if ema_crossover:
            signals.append({
                'direction': 'long',
                'reason': 'EMA golden cross (short > long)',
                'confidence': 1.3,
                'strategy': 'technical'
            })
        else:
            signals.append({
                'direction': 'short',
                'reason': 'EMA death cross (short < long)',
                'confidence': 1.3,
                'strategy': 'technical'
            })
        
        # Bollinger Bands signals
        if bb_position == 'lower':
            signals.append({
                'direction': 'long',
                'reason': 'Price below lower Bollinger Band',
                'confidence': 1.1,
                'strategy': 'technical'
            })
        elif bb_position == 'upper':
            signals.append({
                'direction': 'short',
                'reason': 'Price above upper Bollinger Band',
                'confidence': 1.1,
                'strategy': 'technical'
            })
        
        return signals
    
    def aggregate_signals(self, all_signals: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Aggregate signals from different strategies with weighted scoring"""
        if not all_signals:
            return {'signal': None, 'reason': 'No signals generated'}
        
        long_score = 0
        short_score = 0
        reasons = []
        
        for signal in all_signals:
            weight = self.strategy_weights.get(signal['strategy'], 1.0)
            weighted_confidence = signal['confidence'] * weight
            
            if signal['direction'] == 'long':
                long_score += weighted_confidence
            else:
                short_score += weighted_confidence
            
            reasons.append(f"{signal['strategy']}: {signal['reason']} (confidence: {signal['confidence']:.1f})")
        
        # Determine final signal
        if long_score > short_score and long_score > 2.0:  # Minimum threshold
            final_signal = 'long'
            confidence = min(long_score, 5.0)  # Cap at 5.0
        elif short_score > long_score and short_score > 2.0:
            final_signal = 'short'
            confidence = min(short_score, 5.0)
        else:
            final_signal = None
            confidence = 0
        
        return {
            'signal': final_signal,
            'confidence': confidence,
            'long_score': long_score,
            'short_score': short_score,
            'reasons': reasons,
            'signal_count': len(all_signals),
            'timestamp': datetime.now(timezone.utc).isoformat()
        }

def run_signal_loop(cfg):
    """
    Main signal detection loop with comprehensive analysis
    """
    detector = EnhancedETHPerpSignalDetector()
    
    try:
        print("[SIGNAL] Starting ETH Perpetuals signal detection...")
        
        # Get all signal types
        all_signals = []
        
        # 1. Drift-specific signals
        drift_funding_signals = detector.drift_strategy.analyze_funding_arbitrage()
        if drift_funding_signals.get('signals'):
            all_signals.extend(drift_funding_signals['signals'])
            
        drift_momentum_signals = detector.drift_strategy.analyze_momentum()
        if drift_momentum_signals.get('signals'):
            all_signals.extend(drift_momentum_signals['signals'])
        
        # 2. Cross-exchange arbitrage signals
        cross_exchange_analysis = detector.multi_source_analyzer.analyze_cross_exchange_arbitrage()
        if cross_exchange_analysis.get('signals'):
            all_signals.extend(cross_exchange_analysis['signals'])
        
        # 3. Technical analysis signals
        technical_indicators = detector.calculate_technical_indicators()
        technical_signals = detector.generate_technical_signals(technical_indicators)
        all_signals.extend(technical_signals)
        
        # 4. Aggregate all signals
        final_analysis = detector.aggregate_signals(all_signals)
        
        # Log the analysis
        log_entry = {
            'signal': final_analysis.get('signal'),
            'confidence': final_analysis.get('confidence', 0),
            'signal_count': final_analysis.get('signal_count', 0),
            'strategies_used': list(set(s['strategy'] for s in all_signals)),
            'timestamp': datetime.now(timezone.utc).isoformat()
        }
        
        log_signal(log_entry)
        
        # Print results
        if final_analysis['signal']:
            print(f"[SIGNAL] {final_analysis['signal'].upper()} signal generated!")
            print(f"[SIGNAL] Confidence: {final_analysis['confidence']:.2f}")
            print(f"[SIGNAL] Based on {final_analysis['signal_count']} individual signals")
            
            if cfg.DRY_RUN:
                # Execute simulated trade
                from core.simulation_engine import simulator
                
                # Calculate trade size based on confidence
                base_size = getattr(cfg, 'TRADE_SIZE_USD', 100)
                confidence_multiplier = min(final_analysis['confidence'] / 3.0, 2.0)  # Cap at 2x
                trade_size = base_size * confidence_multiplier
                
                print(f"[DRY RUN] Executing simulated {final_analysis['signal']} trade: ${trade_size:.2f}")
                
                position_id = simulator.open_position(
                    symbol="ETH",
                    side=final_analysis['signal'],
                    trade_size_usd=trade_size,
                    leverage=getattr(cfg, 'LEVERAGE', 1.0),
                    stop_loss_pct=getattr(cfg, 'STOP_LOSS_PCT', 0.02),
                    take_profit_pct=getattr(cfg, 'TAKE_PROFIT_PCT', 0.04)
                )
                
                if position_id:
                    print(f"[DRY RUN] ✅ Position opened: {position_id}")
                else:
                    print(f"[DRY RUN] ❌ Failed to open position")
            else:
                print(f"[LIVE] Signal ready for execution: {final_analysis['signal']}")
                # TODO: Implement live trading logic here
        else:
            print("[SIGNAL] No strong signal detected")
        
        # Print detailed analysis
        if cfg.get('VERBOSE', False):
            print("\n--- Detailed Analysis ---")
            for reason in final_analysis.get('reasons', []):
                print(f"  • {reason}")
            
            if technical_indicators:
                print(f"\nTechnical Indicators:")
                print(f"  RSI: {technical_indicators['rsi']:.1f}")
                print(f"  EMA Cross: {'Bullish' if technical_indicators['ema_crossover'] else 'Bearish'}")
                print(f"  BB Position: {technical_indicators['bb_position']}")
        
        return final_analysis
        
    except Exception as e:
        print(f"[ERROR] Signal detection failed: {e}")
        log_signal({'error': str(e), 'timestamp': datetime.now(timezone.utc).isoformat()})
        return {'signal': None, 'reason': f'Error: {e}'}

if __name__ == "__main__":
    # Test the signal detector
    import sys
    sys.path.append('..')
    
    class TestConfig:
        DRY_RUN = True
        VERBOSE = True
        
    test_cfg = TestConfig()
    result = run_signal_loop(test_cfg)
    print(f"\nFinal Result: {result}")
