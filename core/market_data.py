# core/market_data.py

import pandas as pd
from driftpy.drift_client import DriftClient
from driftpy.wallet import Wallet
from solana.rpc.api import Client as SolanaClient
from config.trade_config import RPC_URL, KEYPAIR_PATH, MARKET_INDEX
from utils.logger import log_trade_action

def init_drift_client():
    solana_client = SolanaClient(RPC_URL)
    wallet = Wallet(KEYPAIR_PATH)
    return DriftClient(solana_client, wallet)

def fetch_eth_perp_ohlcv(limit=100):
    """
    Fetches recent OHLCV data for ETH-PERP from Drift.
    Returns a DataFrame with columns: ['timestamp', 'open', 'high', 'low', 'close', 'volume']
    """
    try:
        drift_client = init_drift_client()
        candles = drift_client.get_candles(market_index=MARKET_INDEX, limit=limit)

        if not candles:
            log_trade_action("No candle data returned from Drift.")
            return pd.DataFrame()

        df = pd.DataFrame([{
            'timestamp': pd.to_datetime(candle.timestamp, unit='s'),
            'open': candle.open,
            'high': candle.high,
            'low': candle.low,
            'close': candle.close,
            'volume': candle.volume
        } for candle in candles])

        return df

    except Exception as e:
        log_trade_action(f"[ERROR] Failed to fetch OHLCV data: {str(e)}")
        return pd.DataFrame()
