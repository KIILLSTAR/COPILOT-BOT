from jupiter_feed import fetch_jupiter_price_data
from signal_detector import detect_market_signal

token_pairs = ["SOL/USDC", "ETH/USDC", "BONK/USDC"]

def scan_all_tokens() -> dict:
    signals = {}
    for pair in token_pairs:
        try:
            price_data = fetch_jupiter_price_data(pair)
            signal = detect_market_signal(price_data)
            signals[pair] = signal
        except Exception as e:
            signals[pair] = "error"
            print(f"⚠️ Error fetching {pair}: {e}")
    return signals
