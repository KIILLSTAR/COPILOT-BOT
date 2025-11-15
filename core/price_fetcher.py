"""
Robust ETH price fetcher with multi-source aggregation, retries, and persistence.
Primary source: Drift (perp mark price). Fallbacks: Jupiter spot, Binance, CoinGecko.
Never raises on network errors; always returns a number (uses last good price or safe default).
"""
from __future__ import annotations

import json
import os
import time
from typing import Optional, Dict, List

import requests


class PriceFetcher:
    def __init__(
        self,
        prefer_perp: bool = True,
        timeout_seconds: float = 5.0,
        max_retries_per_source: int = 2,
        retry_backoff_seconds: float = 0.4,
        last_price_path: str = "data/last_price.json",
    ) -> None:
        self.prefer_perp = prefer_perp
        self.timeout_seconds = timeout_seconds
        self.max_retries_per_source = max_retries_per_source
        self.retry_backoff_seconds = retry_backoff_seconds
        # Allow environment overrides for operational tuning
        env_timeout = os.getenv("ETH_PRICE_TIMEOUT_SECONDS")
        env_retries = os.getenv("ETH_PRICE_MAX_RETRIES")
        env_backoff = os.getenv("ETH_PRICE_RETRY_BACKOFF_SECONDS")
        env_last_path = os.getenv("ETH_PRICE_LAST_PATH")

        self.last_price_path = env_last_path or last_price_path
        self.last_good_price: Optional[float] = None
        self.last_fetch_epoch: Optional[float] = None
        self.session = requests.Session()
        self.session.headers.update({"Accept": "application/json", "Content-Type": "application/json"})
        self.eth_mint = "7vfCXTUXx5WJV5JADk17DUJ4ksgau7utNKj4b963voxs"  # ETH (Wormhole)

        # Apply env overrides after attributes exist
        try:
            if env_timeout is not None:
                self.timeout_seconds = float(env_timeout)
            if env_retries is not None:
                self.max_retries_per_source = int(env_retries)
            if env_backoff is not None:
                self.retry_backoff_seconds = float(env_backoff)
        except Exception:
            # Ignore malformed env values
            pass

        self._ensure_data_dir()
        self._load_last_price()

    def _ensure_data_dir(self) -> None:
        try:
            data_dir = os.path.dirname(self.last_price_path)
            if data_dir and not os.path.exists(data_dir):
                os.makedirs(data_dir, exist_ok=True)
        except Exception:
            # Non-fatal; persistence is best-effort
            pass

    def _load_last_price(self) -> None:
        try:
            if os.path.exists(self.last_price_path):
                with open(self.last_price_path, "r") as f:
                    payload = json.load(f)
                price = float(payload.get("price", 0))
                if price > 0:
                    self.last_good_price = price
                    self.last_fetch_epoch = float(payload.get("epoch", time.time()))
        except Exception:
            # Ignore persistence errors
            pass

    def _save_last_price(self, price: float) -> None:
        try:
            payload = {"price": float(price), "epoch": time.time()}
            with open(self.last_price_path, "w") as f:
                json.dump(payload, f)
        except Exception:
            # Ignore persistence errors
            pass

    # ===== Source fetchers =====
    def _fetch_from_drift(self) -> Optional[float]:
        """Fetch ETH-PERP mark price from Drift (dlob)."""
        try:
            resp = self.session.get(
                "https://dlob.drift.trade/markets/perp/2",
                timeout=self.timeout_seconds,
            )
            if resp.status_code == 200:
                data = resp.json().get("market", {})
                # Prices are 6 decimals
                mark_price = float(data.get("markPrice", 0)) / 1e6
                if mark_price > 0:
                    return mark_price
        except Exception:
            return None
        return None

    def _fetch_from_jupiter_spot(self) -> Optional[float]:
        """Fetch ETH spot price from Jupiter price API."""
        try:
            resp = self.session.get(
                "https://price.jup.ag/v4/price",
                params={"ids": self.eth_mint},
                timeout=self.timeout_seconds,
            )
            if resp.status_code == 200:
                j = resp.json()
                price = (
                    j.get("data", {})
                    .get(self.eth_mint, {})
                    .get("price")
                )
                if price is not None:
                    price = float(price)
                    if price > 0:
                        return price
        except Exception:
            return None
        return None

    def _fetch_from_binance(self) -> Optional[float]:
        try:
            resp = self.session.get(
                "https://api.binance.com/api/v3/ticker/price",
                params={"symbol": "ETHUSDT"},
                timeout=self.timeout_seconds,
            )
            if resp.status_code == 200:
                price = float(resp.json().get("price", 0))
                if price > 0:
                    return price
        except Exception:
            return None
        return None

    def _fetch_from_coingecko(self) -> Optional[float]:
        try:
            resp = self.session.get(
                "https://api.coingecko.com/api/v3/simple/price",
                params={"ids": "ethereum", "vs_currencies": "usd"},
                timeout=self.timeout_seconds,
            )
            if resp.status_code == 200:
                price = float(resp.json().get("ethereum", {}).get("usd", 0))
                if price > 0:
                    return price
        except Exception:
            return None
        return None

    def _attempt_with_retries(self, fn) -> Optional[float]:
        attempts = 0
        delay = self.retry_backoff_seconds
        while attempts <= self.max_retries_per_source:
            result = fn()
            if isinstance(result, (int, float)) and result > 0:
                return float(result)
            attempts += 1
            if attempts <= self.max_retries_per_source:
                try:
                    time.sleep(delay)
                except Exception:
                    pass
                delay *= 1.8
        return None

    def _gather_candidates(self) -> List[float]:
        # Preference order: perp (Drift) -> Jupiter spot -> Binance -> CoinGecko
        sources = [self._fetch_from_drift, self._fetch_from_jupiter_spot, self._fetch_from_binance, self._fetch_from_coingecko]
        prices: List[float] = []
        for fetch_fn in sources:
            price = self._attempt_with_retries(fetch_fn)
            if price is not None and price > 0:
                prices.append(price)
        return prices

    def get_eth_price(self) -> float:
        """
        Return a robust ETH price.
        - Tries multiple sources with retries.
        - Chooses median of gathered candidates for robustness.
        - Falls back to last good price if available.
        - If nothing available, returns a safe default (3000.0).
        """
        prices = self._gather_candidates()

        selected: Optional[float] = None
        if prices:
            # Median for robustness against outliers
            prices.sort()
            mid = len(prices) // 2
            selected = prices[mid] if len(prices) % 2 == 1 else (prices[mid - 1] + prices[mid]) / 2.0
        elif self.last_good_price is not None:
            print(f"⚠️ Price APIs unavailable. Using last known price: ${self.last_good_price:,.2f}")
            selected = self.last_good_price
        else:
            print("⚠️ No price data available. Using fallback price: $3,000.00")
            selected = 3000.0

        # Persist and update last_good_price
        if selected is not None and selected > 0:
            self.last_good_price = selected
            self.last_fetch_epoch = time.time()
            self._save_last_price(selected)
            return float(selected)

        # Absolute fallback guard
        return 3000.0


# Global singleton
price_fetcher = PriceFetcher()
