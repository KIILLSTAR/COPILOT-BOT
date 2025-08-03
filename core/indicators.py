"""
Technical Indicators for ETH Perpetuals Trading
Supports both Drift Protocol and Jupiter ecosystem data
"""
import pandas as pd
import numpy as np
from typing import Tuple, Optional

def calculate_rsi(prices: pd.Series, period: int = 14) -> pd.Series:
    """
    Calculate Relative Strength Index (RSI)
    """
    delta = prices.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def calculate_ema(prices: pd.Series, period: int) -> pd.Series:
    """
    Calculate Exponential Moving Average (EMA)
    """
    return prices.ewm(span=period, adjust=False).mean()

def calculate_sma(prices: pd.Series, period: int) -> pd.Series:
    """
    Calculate Simple Moving Average (SMA)
    """
    return prices.rolling(window=period).mean()

def calculate_bollinger_bands(prices: pd.Series, period: int = 20, std_dev: float = 2) -> Tuple[pd.Series, pd.Series, pd.Series]:
    """
    Calculate Bollinger Bands
    Returns: (upper_band, middle_band, lower_band)
    """
    middle_band = calculate_sma(prices, period)
    std = prices.rolling(window=period).std()
    
    upper_band = middle_band + (std * std_dev)
    lower_band = middle_band - (std * std_dev)
    
    return upper_band, middle_band, lower_band

def calculate_macd(prices: pd.Series, fast_period: int = 12, slow_period: int = 26, signal_period: int = 9) -> Tuple[pd.Series, pd.Series, pd.Series]:
    """
    Calculate MACD (Moving Average Convergence Divergence)
    Returns: (macd_line, signal_line, histogram)
    """
    ema_fast = calculate_ema(prices, fast_period)
    ema_slow = calculate_ema(prices, slow_period)
    
    macd_line = ema_fast - ema_slow
    signal_line = calculate_ema(macd_line, signal_period)
    histogram = macd_line - signal_line
    
    return macd_line, signal_line, histogram

def calculate_stochastic(high: pd.Series, low: pd.Series, close: pd.Series, 
                        k_period: int = 14, d_period: int = 3) -> Tuple[pd.Series, pd.Series]:
    """
    Calculate Stochastic Oscillator
    Returns: (%K, %D)
    """
    lowest_low = low.rolling(window=k_period).min()
    highest_high = high.rolling(window=k_period).max()
    
    k_percent = 100 * ((close - lowest_low) / (highest_high - lowest_low))
    d_percent = k_percent.rolling(window=d_period).mean()
    
    return k_percent, d_percent

def calculate_atr(high: pd.Series, low: pd.Series, close: pd.Series, period: int = 14) -> pd.Series:
    """
    Calculate Average True Range (ATR)
    """
    tr1 = high - low
    tr2 = abs(high - close.shift())
    tr3 = abs(low - close.shift())
    
    true_range = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    atr = true_range.rolling(window=period).mean()
    
    return atr

def calculate_vwap(prices: pd.Series, volumes: pd.Series) -> pd.Series:
    """
    Calculate Volume Weighted Average Price (VWAP)
    """
    return (prices * volumes).cumsum() / volumes.cumsum()

def calculate_funding_rate_indicators(funding_rates: pd.Series, period: int = 24) -> dict:
    """
    Calculate funding rate specific indicators for perpetuals
    """
    # Convert to annualized rates for easier interpretation
    annualized_rates = funding_rates * 365 * 24  # Assuming hourly funding
    
    return {
        'current_funding_annual': annualized_rates.iloc[-1] if len(annualized_rates) > 0 else 0,
        'avg_funding_24h': annualized_rates.tail(period).mean(),
        'funding_volatility': annualized_rates.tail(period).std(),
        'funding_trend': 'increasing' if len(annualized_rates) >= 2 and annualized_rates.iloc[-1] > annualized_rates.iloc[-2] else 'decreasing',
        'extreme_funding': abs(annualized_rates.iloc[-1]) > 0.5 if len(annualized_rates) > 0 else False  # 50% annual
    }

def calculate_oi_indicators(open_interest: pd.Series, prices: pd.Series) -> dict:
    """
    Calculate Open Interest indicators for perpetuals
    """
    if len(open_interest) < 2 or len(prices) < 2:
        return {}
    
    oi_change = open_interest.pct_change()
    price_change = prices.pct_change()
    
    # Align series
    min_len = min(len(oi_change), len(price_change))
    oi_change = oi_change.tail(min_len)
    price_change = price_change.tail(min_len)
    
    return {
        'oi_trend': 'increasing' if oi_change.iloc[-1] > 0 else 'decreasing',
        'oi_price_divergence': (oi_change.iloc[-1] > 0 and price_change.iloc[-1] < 0) or 
                              (oi_change.iloc[-1] < 0 and price_change.iloc[-1] > 0),
        'oi_momentum': oi_change.tail(5).mean(),  # Average OI change over last 5 periods
        'price_oi_correlation': oi_change.tail(20).corr(price_change.tail(20)) if len(oi_change) >= 20 else 0
    }

def calculate_market_structure(highs: pd.Series, lows: pd.Series, closes: pd.Series) -> dict:
    """
    Calculate market structure indicators (higher highs, lower lows, etc.)
    """
    if len(closes) < 10:
        return {}
    
    # Recent highs and lows
    recent_high = highs.tail(20).max()
    recent_low = lows.tail(20).min()
    current_price = closes.iloc[-1]
    
    # Swing points
    swing_highs = []
    swing_lows = []
    
    for i in range(2, len(highs) - 2):
        # Swing high: higher than 2 periods before and after
        if highs.iloc[i] > highs.iloc[i-1] and highs.iloc[i] > highs.iloc[i-2] and \
           highs.iloc[i] > highs.iloc[i+1] and highs.iloc[i] > highs.iloc[i+2]:
            swing_highs.append((i, highs.iloc[i]))
        
        # Swing low: lower than 2 periods before and after
        if lows.iloc[i] < lows.iloc[i-1] and lows.iloc[i] < lows.iloc[i-2] and \
           lows.iloc[i] < lows.iloc[i+1] and lows.iloc[i] < lows.iloc[i+2]:
            swing_lows.append((i, lows.iloc[i]))
    
    # Determine trend structure
    trend = 'sideways'
    if len(swing_highs) >= 2 and len(swing_lows) >= 2:
        recent_swing_highs = sorted(swing_highs, key=lambda x: x[0])[-2:]
        recent_swing_lows = sorted(swing_lows, key=lambda x: x[0])[-2:]
        
        if (recent_swing_highs[1][1] > recent_swing_highs[0][1] and 
            recent_swing_lows[1][1] > recent_swing_lows[0][1]):
            trend = 'uptrend'
        elif (recent_swing_highs[1][1] < recent_swing_highs[0][1] and 
              recent_swing_lows[1][1] < recent_swing_lows[0][1]):
            trend = 'downtrend'
    
    return {
        'trend_structure': trend,
        'distance_from_high': (recent_high - current_price) / recent_high,
        'distance_from_low': (current_price - recent_low) / current_price,
        'swing_high_count': len(swing_highs),
        'swing_low_count': len(swing_lows)
    }

def calculate_volatility_indicators(prices: pd.Series, period: int = 20) -> dict:
    """
    Calculate various volatility indicators
    """
    returns = prices.pct_change().dropna()
    
    if len(returns) < period:
        return {}
    
    rolling_vol = returns.rolling(window=period).std()
    
    return {
        'current_volatility': rolling_vol.iloc[-1] * np.sqrt(365) if len(rolling_vol) > 0 else 0,  # Annualized
        'volatility_percentile': (rolling_vol.iloc[-1] > rolling_vol.quantile(0.8)) if len(rolling_vol) > 0 else False,
        'volatility_trend': 'increasing' if len(rolling_vol) >= 2 and rolling_vol.iloc[-1] > rolling_vol.iloc[-2] else 'decreasing',
        'vol_of_vol': rolling_vol.rolling(window=10).std().iloc[-1] if len(rolling_vol) >= 10 else 0
    }

class TechnicalAnalysisEngine:
    """
    Comprehensive technical analysis engine for ETH perpetuals
    Supports both Drift and Jupiter data
    """
    
    def __init__(self):
        self.lookback_period = 100
        
    def analyze_price_action(self, price_data: list, volume_data: list = None) -> dict:
        """
        Comprehensive price action analysis
        """
        if len(price_data) < 20:
            return {'error': 'Insufficient data for analysis'}
        
        prices = pd.Series(price_data)
        volumes = pd.Series(volume_data) if volume_data else None
        
        # Basic indicators
        rsi = calculate_rsi(prices)
        ema_9 = calculate_ema(prices, 9)
        ema_21 = calculate_ema(prices, 21)
        bb_upper, bb_middle, bb_lower = calculate_bollinger_bands(prices)
        macd, macd_signal, macd_hist = calculate_macd(prices)
        
        # Market structure
        highs = prices  # Assuming price data represents close prices
        lows = prices   # In real implementation, you'd have separate OHLC data
        market_structure = calculate_market_structure(highs, lows, prices)
        
        # Volatility
        volatility = calculate_volatility_indicators(prices)
        
        current_price = prices.iloc[-1]
        
        analysis = {
            'current_price': current_price,
            'rsi': rsi.iloc[-1] if len(rsi) > 0 else 50,
            'ema_9': ema_9.iloc[-1] if len(ema_9) > 0 else current_price,
            'ema_21': ema_21.iloc[-1] if len(ema_21) > 0 else current_price,
            'bb_upper': bb_upper.iloc[-1] if len(bb_upper) > 0 else current_price,
            'bb_lower': bb_lower.iloc[-1] if len(bb_lower) > 0 else current_price,
            'macd': macd.iloc[-1] if len(macd) > 0 else 0,
            'macd_signal': macd_signal.iloc[-1] if len(macd_signal) > 0 else 0,
            'macd_histogram': macd_hist.iloc[-1] if len(macd_hist) > 0 else 0,
            'market_structure': market_structure,
            'volatility': volatility,
            'signals': self._generate_signals(prices, rsi, ema_9, ema_21, bb_upper, bb_lower, macd, macd_hist)
        }
        
        if volumes is not None:
            analysis['vwap'] = calculate_vwap(prices, volumes).iloc[-1]
        
        return analysis
    
    def _generate_signals(self, prices, rsi, ema_9, ema_21, bb_upper, bb_lower, macd, macd_hist) -> list:
        """
        Generate trading signals based on technical indicators
        """
        signals = []
        
        if len(prices) < 2:
            return signals
        
        current_price = prices.iloc[-1]
        
        # RSI signals
        if len(rsi) > 0:
            current_rsi = rsi.iloc[-1]
            if current_rsi < 30:
                signals.append({
                    'type': 'oversold',
                    'indicator': 'RSI',
                    'direction': 'bullish',
                    'strength': min((30 - current_rsi) / 10, 2.0)
                })
            elif current_rsi > 70:
                signals.append({
                    'type': 'overbought', 
                    'indicator': 'RSI',
                    'direction': 'bearish',
                    'strength': min((current_rsi - 70) / 10, 2.0)
                })
        
        # EMA crossover signals
        if len(ema_9) > 0 and len(ema_21) > 0:
            current_ema_9 = ema_9.iloc[-1]
            current_ema_21 = ema_21.iloc[-1]
            
            if current_ema_9 > current_ema_21:
                signals.append({
                    'type': 'golden_cross',
                    'indicator': 'EMA',
                    'direction': 'bullish', 
                    'strength': 1.2
                })
            else:
                signals.append({
                    'type': 'death_cross',
                    'indicator': 'EMA',
                    'direction': 'bearish',
                    'strength': 1.2
                })
        
        # Bollinger Bands signals
        if len(bb_upper) > 0 and len(bb_lower) > 0:
            current_bb_upper = bb_upper.iloc[-1]
            current_bb_lower = bb_lower.iloc[-1]
            
            if current_price > current_bb_upper:
                signals.append({
                    'type': 'bb_breakout_upper',
                    'indicator': 'Bollinger_Bands',
                    'direction': 'bearish',  # Potential reversal
                    'strength': 1.1
                })
            elif current_price < current_bb_lower:
                signals.append({
                    'type': 'bb_breakout_lower',
                    'indicator': 'Bollinger_Bands', 
                    'direction': 'bullish',  # Potential reversal
                    'strength': 1.1
                })
        
        # MACD signals
        if len(macd) > 1 and len(macd_hist) > 1:
            if macd_hist.iloc[-1] > 0 and macd_hist.iloc[-2] <= 0:
                signals.append({
                    'type': 'macd_bullish_crossover',
                    'indicator': 'MACD',
                    'direction': 'bullish',
                    'strength': 1.3
                })
            elif macd_hist.iloc[-1] < 0 and macd_hist.iloc[-2] >= 0:
                signals.append({
                    'type': 'macd_bearish_crossover',
                    'indicator': 'MACD',
                    'direction': 'bearish',
                    'strength': 1.3
                })
        
        return signals

# Example usage
if __name__ == "__main__":
    # Test with sample data
    import random
    
    # Generate sample price data
    base_price = 3500
    prices = [base_price]
    for i in range(50):
        change = random.uniform(-0.02, 0.02)  # ±2% change
        new_price = prices[-1] * (1 + change)
        prices.append(new_price)
    
    engine = TechnicalAnalysisEngine()
    analysis = engine.analyze_price_action(prices)
    
    print("Technical Analysis Results:")
    print(f"Current Price: ${analysis['current_price']:.2f}")
    print(f"RSI: {analysis['rsi']:.1f}")
    print(f"EMA 9: ${analysis['ema_9']:.2f}")
    print(f"EMA 21: ${analysis['ema_21']:.2f}")
    print(f"Market Structure: {analysis['market_structure'].get('trend_structure', 'unknown')}")
    
    print("\nSignals Generated:")
    for signal in analysis['signals']:
        print(f"  {signal['type']}: {signal['direction']} (strength: {signal['strength']:.1f})")
