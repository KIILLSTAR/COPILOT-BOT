# indicators.py

import pandas_ta as ta
import pandas as pd

def calculate_indicators(df: pd.DataFrame) -> pd.DataFrame:
    df["RSI"] = ta.rsi(df["price"], length=14)
    df["EMA_fast"] = ta.ema(df["price"], length=9)
    df["EMA_slow"] = ta.ema(df["price"], length=21)

    # Volume spike detection
    avg_volume = df["volume"].rolling(window=20).mean()
    df["Volume_Spike"] = df["volume"] > (avg_volume * 1.5)

    df.fillna(0, inplace=True)
    return df
