# market_data.py

import pandas as pd
import requests

def fetch_price_data():
    url = "https://api.coingecko.com/api/v3/coins/ethereum/market_chart"
    params = {"vs_currency": "usd", "days": "1", "interval": "minute"}
    response = requests.get(url, params=params)
    data = response.json()
    prices = data["prices"]
    volumes = data["total_volumes"]

    df = pd.DataFrame({
        "timestamp": [p[0] for p in prices],
        "price": [p[1] for p in prices],
        "volume": [v[1] for v in volumes]
    })
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    return df

def build_market_dataframe():
    df = fetch_price_data()
    return df.tail(100)  # use last 100 minutes
