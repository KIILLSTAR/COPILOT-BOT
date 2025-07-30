# strategy/eth_strategy.py

import pandas as pd
import numpy as np
from core.market_data import fetch_eth_perp_ohlcv

### 📊 Strategy Parameters
RSI_PERIOD = 14
EMA_FAST = 9
EMA_SLOW = 21
VOLUME_SPIKE_MULTIPLIER = 1.5

def fetch_eth_perp_data():
    """
    Placeholder: Replace with real Drift or market data fetch.
    Returns OHLCV DataFrame with columns: ['timestamp', 'open', 'high', 'low', 'close', 'volume']
    """
    # Simulated data for testing
    data = {
        'timestamp': pd.date_range(end=pd.Timestamp.now(), periods=100, freq='1min'),
        'open': np.random.uniform(1800, 1900, 100),
        'high': np.random.uniform(1900, 1950, 100),
        'low': np.random.uniform(1750, 1850, 100),
        'close': np.random.uniform(1800, 1900, 100),
        'volume': np.random.uniform(100, 500, 100)
    }
    return pd.DataFrame(data)

def calculate_rsi(df, period=RSI_PERIOD):
    delta = df['close'].diff()
    gain = np.where(delta > 0, delta, 0)
    loss = np.where(delta < 0, -delta, 0)

    avg_gain = pd.Series(gain).rolling(window=period).mean()
    avg_loss = pd.Series(loss).rolling(window=period).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def generate_signal():
    df = fetch_eth_perp_data()

    if df is None or df.empty:
        log_trade_action("No market data available.")
        return None

    df['ema_fast'] = df['close'].ewm(span=EMA_FAST, adjust=False).mean()
    df['ema_slow'] = df['close'].ewm(span=EMA_SLOW, adjust=False).mean()
    df['rsi'] = calculate_rsi(df)
    df['volume_avg'] = df['volume'].rolling(window=20).mean()

    latest = df.iloc[-1]

    ### 🔍 Signal Conditions
    rsi_signal = None
    ema_signal = None
    volume_signal = None

    # RSI-based signal
    if latest['rsi'] < 30:
        rsi_signal = "long"
    elif latest['rsi'] > 70:
        rsi_signal = "short"

    # EMA crossover signal
    if latest['ema_fast'] > latest['ema_slow']:
        ema_signal = "long"
    elif latest['ema_fast'] < latest['ema_slow']:
        ema_signal = "short"

    # Volume spike signal
    if latest['volume'] > latest['volume_avg'] * VOLUME_SPIKE_MULTIPLIER:
        volume_signal = "confirm
