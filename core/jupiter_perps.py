"""
Jupiter Perpetuals API Client
Replaces Drift Protocol entirely — all perp data comes from Jupiter.
Docs: https://perps-api.jup.ag
"""
from __future__ import annotations
import requests
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
from datetime import datetime, timezone

@dataclass
class PerpMarket:
    symbol: str
    mark_price: float
    index_price: float
    funding_rate: float       # hourly rate as decimal
    open_interest_long: float
    open_interest_short: float
    volume_24h: float
    price_change_24h_pct: float
    timestamp: str

@dataclass
class PerpPosition:
    market: str
    side: str           # "long" or "short"
    size_usd: float
    entry_price: float
    mark_price: float
    leverage: float
    unrealized_pnl: float
    liquidation_price: float

class JupiterPerpsClient:
    BASE = "https://perps-api.jup.ag/v1"

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({"Accept": "application/json"})

    def get_markets(self) -> List[Dict]:
        """Get all Jupiter perp markets."""
        try:
            r = self.session.get(f"{self.BASE}/markets", timeout=8)
            if r.status_code == 200:
                return r.json()
        except Exception as e:
            print(f"[JupiterPerps] get_markets error: {e}")
        return []

    def get_eth_market(self) -> Optional[PerpMarket]:
        """Get ETH-PERP market data."""
        try:
            markets = self.get_markets()
            for m in markets:
                sym = m.get("symbol", "").upper()
                if "ETH" in sym:
                    return PerpMarket(
                        symbol=m.get("symbol", "ETH-PERP"),
                        mark_price=float(m.get("markPrice") or 0),
                        index_price=float(m.get("indexPrice") or 0),
                        funding_rate=float(m.get("fundingRate") or 0),
                        open_interest_long=float(m.get("openInterestLong") or 0),
                        open_interest_short=float(m.get("openInterestShort") or 0),
                        volume_24h=float(m.get("volume24h") or 0),
                        price_change_24h_pct=float(m.get("priceChange24h") or 0),
                        timestamp=datetime.now(timezone.utc).isoformat()
                    )
        except Exception as e:
            print(f"[JupiterPerps] get_eth_market error: {e}")
        return None

    def get_funding_rate(self, symbol: str = "ETH-PERP") -> float:
        """Get current hourly funding rate for a market."""
        try:
            market = self.get_eth_market()
            if market:
                return market.funding_rate
        except Exception:
            pass
        return 0.0

    def get_open_interest(self, symbol: str = "ETH-PERP") -> Dict[str, float]:
        """Get long/short open interest."""
        try:
            market = self.get_eth_market()
            if market:
                return {
                    "long": market.open_interest_long,
                    "short": market.open_interest_short,
                    "ratio": market.open_interest_long / max(market.open_interest_short, 1)
                }
        except Exception:
            pass
        return {"long": 0, "short": 0, "ratio": 1.0}

    def get_market_summary(self) -> Dict[str, Any]:
        """Full market snapshot for dashboard display."""
        market = self.get_eth_market()
        if not market:
            return {"error": "Could not fetch Jupiter perp data"}
        oi = self.get_open_interest()
        sentiment = "NEUTRAL"
        if oi["ratio"] > 1.3:
            sentiment = "LONG-HEAVY"
        elif oi["ratio"] < 0.7:
            sentiment = "SHORT-HEAVY"
        return {
            "symbol": market.symbol,
            "mark_price": market.mark_price,
            "index_price": market.index_price,
            "funding_rate_hourly": market.funding_rate,
            "funding_rate_daily": market.funding_rate * 24,
            "open_interest_long": market.open_interest_long,
            "open_interest_short": market.open_interest_short,
            "oi_ratio": round(oi["ratio"], 3),
            "market_sentiment": sentiment,
            "volume_24h": market.volume_24h,
            "price_change_24h_pct": market.price_change_24h_pct,
            "timestamp": market.timestamp
        }

# Singleton
jupiter_perps = JupiterPerpsClient()
