"""
Signal Detector — Jupiter-native, no Drift dependency.
Combines: RSI, EMA crossover, Bollinger Bands, funding rate bias, OI ratio.
Returns a signal dict with direction and confidence score.
"""
from __future__ import annotations
import requests
import numpy as np
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
from core.price_fetcher import price_fetcher
from core.jupiter_perps import jupiter_perps

def _fetch_price_history(limit: int = 50) -> List[float]:
    """Get recent ETH prices from Binance (reliable OHLC source)."""
    try:
        r = requests.get(
            "https://fapi.binance.com/fapi/v1/klines",
            params={"symbol": "ETHUSDT", "interval": "1m", "limit": limit},
            timeout=6
        )
        if r.status_code == 200:
            return [float(k[4]) for k in r.json()]  # close prices
    except Exception:
        pass
    # Fallback: synthetic prices around current
    base = price_fetcher.get_eth_price()
    return [base * (1 + (i - 25) * 0.0001) for i in range(limit)]

def _rsi(prices: List[float], period: int = 14) -> float:
    if len(prices) < period + 1:
        return 50.0
    deltas = [prices[i] - prices[i-1] for i in range(1, len(prices))]
    gains = [d for d in deltas[-period:] if d > 0]
    losses = [-d for d in deltas[-period:] if d < 0]
    avg_gain = sum(gains) / period if gains else 0
    avg_loss = sum(losses) / period if losses else 1e-9
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))

def _ema(prices: List[float], period: int) -> float:
    if len(prices) < period:
        return prices[-1] if prices else 0
    k = 2 / (period + 1)
    ema = prices[0]
    for p in prices[1:]:
        ema = p * k + ema * (1 - k)
    return ema

def _bollinger(prices: List[float], period: int = 20) -> Dict:
    if len(prices) < period:
        mid = prices[-1]
        return {"upper": mid * 1.02, "mid": mid, "lower": mid * 0.98, "pct_b": 0.5}
    window = prices[-period:]
    mid = sum(window) / period
    std = (sum((p - mid)**2 for p in window) / period) ** 0.5
    upper = mid + 2 * std
    lower = mid - 2 * std
    current = prices[-1]
    pct_b = (current - lower) / (upper - lower) if upper != lower else 0.5
    return {"upper": upper, "mid": mid, "lower": lower, "pct_b": pct_b}

def detect_signal(cfg) -> Dict[str, Any]:
    """
    Run full signal detection. Returns:
    {
      "direction": "long" | "short" | "none",
      "confidence": 0.0-1.0,
      "reason": str,
      "indicators": {...}
    }
    """
    prices = _fetch_price_history(50)
    current_price = prices[-1] if prices else price_fetcher.get_eth_price()

    rsi = _rsi(prices)
    ema9 = _ema(prices, 9)
    ema21 = _ema(prices, 21)
    bb = _bollinger(prices)

    # Jupiter perp market data
    market = jupiter_perps.get_market_summary()
    funding = market.get("funding_rate_hourly", 0)
    oi_ratio = market.get("oi_ratio", 1.0)  # >1 = more longs

    # --- Scoring ---
    long_score = 0.0
    short_score = 0.0
    reasons = []

    # RSI
    if rsi < 35:
        long_score += 0.25
        reasons.append(f"RSI oversold ({rsi:.1f})")
    elif rsi > 65:
        short_score += 0.25
        reasons.append(f"RSI overbought ({rsi:.1f})")

    # EMA crossover
    if ema9 > ema21:
        long_score += 0.20
        reasons.append("EMA9 > EMA21 (bullish)")
    else:
        short_score += 0.20
        reasons.append("EMA9 < EMA21 (bearish)")

    # Bollinger Bands
    if bb["pct_b"] < 0.15:
        long_score += 0.20
        reasons.append(f"Near BB lower ({bb['pct_b']:.2f})")
    elif bb["pct_b"] > 0.85:
        short_score += 0.20
        reasons.append(f"Near BB upper ({bb['pct_b']:.2f})")

    # Funding rate (negative = longs pay shorts → short pressure)
    if funding < -0.0001:
        short_score += 0.15
        reasons.append(f"Negative funding ({funding:.4f})")
    elif funding > 0.0001:
        long_score += 0.10
        reasons.append(f"Positive funding ({funding:.4f})")

    # OI ratio (heavily long-biased market = mean reversion short opportunity)
    if oi_ratio > 1.5:
        short_score += 0.10
        reasons.append(f"OI long-heavy ({oi_ratio:.2f}x)")
    elif oi_ratio < 0.6:
        long_score += 0.10
        reasons.append(f"OI short-heavy ({oi_ratio:.2f}x)")

    # Determine direction
    threshold = cfg.SIGNAL_THRESHOLD
    if long_score >= threshold and long_score > short_score:
        direction = "long"
        confidence = min(long_score, 1.0)
    elif short_score >= threshold and short_score > long_score:
        direction = "short"
        confidence = min(short_score, 1.0)
    else:
        direction = "none"
        confidence = max(long_score, short_score)

    return {
        "direction": direction,
        "confidence": round(confidence, 3),
        "reason": " | ".join(reasons),
        "indicators": {
            "rsi": round(rsi, 2),
            "ema9": round(ema9, 2),
            "ema21": round(ema21, 2),
            "bb_pct_b": round(bb["pct_b"], 3),
            "funding_rate": funding,
            "oi_ratio": oi_ratio,
            "current_price": round(current_price, 2),
        },
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
