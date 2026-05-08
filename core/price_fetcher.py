"""
Robust ETH price fetcher — Jupiter-native, no Drift dependency.
Sources: Jupiter Perps API → Jupiter Spot → Binance → CoinGecko → cached fallback
"""
from __future__ import annotations
import json, os, time
from typing import Optional
import requests

class PriceFetcher:
    def __init__(self, timeout: float = 5.0, last_price_path: str = "data/last_price.json"):
        self.timeout = timeout
        self.last_price_path = last_price_path
        self.last_good_price: Optional[float] = None
        self.session = requests.Session()
        self.session.headers.update({"Accept": "application/json"})
        # ETH Wormhole mint on Solana
        self.eth_mint = "7vfCXTUXx5WJV5JADk17DUJ4ksgau7utNKj4b963voxs"
        self.usdc_mint = "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"
        os.makedirs(os.path.dirname(last_price_path), exist_ok=True)
        self._load_cached()

    def _load_cached(self):
        try:
            if os.path.exists(self.last_price_path):
                with open(self.last_price_path) as f:
                    d = json.load(f)
                p = float(d.get("price", 0))
                if p > 0:
                    self.last_good_price = p
        except Exception:
            pass

    def _save_cached(self, price: float):
        try:
            with open(self.last_price_path, "w") as f:
                json.dump({"price": price, "ts": time.time()}, f)
        except Exception:
            pass

    # --- Individual sources ---

    def _from_jupiter_perps(self) -> Optional[float]:
        """Jupiter Perps price for ETH-PERP market."""
        try:
            # Jupiter Perps v1 markets endpoint
            r = self.session.get(
                "https://perps-api.jup.ag/v1/markets",
                timeout=self.timeout
            )
            if r.status_code == 200:
                markets = r.json()
                for m in markets:
                    sym = m.get("symbol", "").upper()
                    if "ETH" in sym:
                        price = float(m.get("markPrice") or m.get("indexPrice") or 0)
                        if price > 0:
                            return price
        except Exception:
            pass
        return None

    def _from_jupiter_spot(self) -> Optional[float]:
        """Jupiter Swap quote: 1 ETH → USDC."""
        try:
            params = {
                "inputMint": self.eth_mint,
                "outputMint": self.usdc_mint,
                "amount": 100_000_000,  # 1 ETH in lamports (8 decimals for wETH)
                "slippageBps": 50,
            }
            r = self.session.get("https://quote-api.jup.ag/v6/quote", params=params, timeout=self.timeout)
            if r.status_code == 200:
                d = r.json()
                out = float(d.get("outAmount", 0))
                inp = float(d.get("inAmount", 1))
                if out > 0:
                    return (out / inp) * 1e2  # wETH is 8 dec, USDC is 6 dec → multiply by 100
        except Exception:
            pass
        return None

    def _from_binance(self) -> Optional[float]:
        try:
            r = self.session.get(
                "https://fapi.binance.com/fapi/v1/ticker/price",
                params={"symbol": "ETHUSDT"},
                timeout=self.timeout
            )
            if r.status_code == 200:
                return float(r.json()["price"])
        except Exception:
            pass
        return None

    def _from_coingecko(self) -> Optional[float]:
        try:
            r = self.session.get(
                "https://api.coingecko.com/api/v3/simple/price",
                params={"ids": "ethereum", "vs_currencies": "usd"},
                timeout=self.timeout
            )
            if r.status_code == 200:
                return float(r.json()["ethereum"]["usd"])
        except Exception:
            pass
        return None

    def get_eth_price(self) -> float:
        """Try all sources in order, return best available price."""
        for source in [self._from_jupiter_perps, self._from_binance, self._from_jupiter_spot, self._from_coingecko]:
            try:
                price = source()
                if price and price > 100:  # sanity check
                    self.last_good_price = price
                    self._save_cached(price)
                    return price
            except Exception:
                continue
        # Fallback to last known good price
        return self.last_good_price or 2000.0

    def get_price(self, symbol: str = "ETH") -> float:
        return self.get_eth_price()

# Singleton
price_fetcher = PriceFetcher()
