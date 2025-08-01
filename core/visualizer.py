# visualizer.py

import matplotlib.pyplot as plt

def plot_signal_frequency(stats):
    """
    Plots a bar chart of signal frequency per asset.
    """
    for asset, signals in stats.items():
        labels = list(signals.keys())
        values = list(signals.values())

        plt.figure(figsize=(6, 4))
        plt.bar(labels, values, color='skyblue')
        plt.title(f"Signal Frequency for {asset}")
        plt.xlabel("Signal Type")
        plt.ylabel("Count")
        plt.tight_layout()
        plt.show()

def plot_asset_timeline(parsed_logs):
    """
    Plots a timeline of asset selections.
    """
    times = [entry["time"] for entry in parsed_logs]
    assets = [entry["asset"] for entry in parsed_logs]

    plt.figure(figsize=(10, 2))
    plt.plot(times, assets, marker='o', linestyle='-', color='green')
    plt.title("Asset Selection Timeline")
    plt.xlabel("Time")
    plt.ylabel("Asset")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def plot_pnl_simulation(parsed_logs, price_lookup):
    """
    Simulates PnL based on signal entries and mock price data.
    `price_lookup` should be a dict: {timestamp: {asset: price}}
    """
    pnl = []
    last_price = None
    last_asset = None

    for entry in parsed_logs:
        ts = entry["time"].isoformat()
        asset = entry["asset"]
        price = price_lookup.get(ts, {}).get(asset)

        if price and last_price and last_asset == asset:
            change = price - last_price
            pnl.append(change)
        last_price = price
        last_asset = asset

    plt.figure(figsize=(8, 4))
    plt.plot(pnl, color='orange')
    plt.title("Simulated PnL Over Time")
    plt.xlabel("Trade Index")
    plt.ylabel("PnL")
    plt.tight_layout()
    plt.show()