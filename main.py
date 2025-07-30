# main.py

from config import LIVE_MODE, SECRET_KEY, ETH_MINT, USDC_MINT)
from wallet import load_keypair, get_wallet_address
from jupiter_api import execute_swap
from market_data import build_market_dataframe
from indicators import calculate_indicators
from dry_run import simulate_trade
from logger import log_trade
from performance import evaluate_performance

def generate_signal(df):
    latest = df.iloc[-1]
    if latest['RSI'] < 30 and latest['EMA_fast'] > latest['EMA_slow'] and latest['Volume_Spike']:
        return "BUY"
    elif latest['RSI'] > 70 and latest['EMA_fast'] < latest['EMA_slow']:
        return "SELL"
    else:
        return "HOLD"

def main():
    try:
        keypair = load_keypair(SECRET_KEY)
        wallet_address = get_wallet_address(keypair)

        df = build_market_dataframe()
        df = calculate_indicators(df)

        signal = generate_signal(df)
        asset = "ETH-PERP"
        amount = 1.0

        if signal != "HOLD":
            if LIVE_MODE:
                try:
                    execute_swap(wallet_address, ETH_MINT
