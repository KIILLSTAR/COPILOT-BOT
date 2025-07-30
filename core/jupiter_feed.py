import requests
import pandas as pd

def fetch_jupiter_price_data(token_symbol: str, interval: str = "1m", limit: int = 100) -> pd.DataFrame:
    url = f"https://price.jup.ag/v4/chart?symbol={token_symbol}&interval={interval}&limit={limit}"
    response = requests.get(url)
    data = response.json()["data"]

    df = pd.DataFrame(data)
    df.rename(columns={
        "o": "open",
        "h": "high",
        "l": "low",
        "c": "close",
        "v": "volume"
    }, inplace=True)

    return df[["open", "high", "low", "close", "volume"]]

def fetch_latest_price_snapshot(token_pair: str) -> dict:
    url = f"https://price.jup.ag/v4/chart?symbol={token_pair}&interval=1m&limit=1"
    response = requests.get(url)
    data = response.json()["data"][0]  # latest candle

    return {
        "open": data["o"],
        "high": data["h"],
        "low": data["l"],
        "close": data["c"],
        "volume": data["v"]
    }
