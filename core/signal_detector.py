from wallet.logger import log_info, log_event
log_info("Signal detected for SOL")

def detect_market_signal(price_data: pd.DataFrame) -> str:
    # Apply indicators
    price_data.ta.rsi(length=14, append=True)
    price_data.ta.ema(length=21, append=True)
    price_data.ta.volume(append=True)

    latest_rsi = price_data["RSI_14"].iloc[-1]
    latest_ema = price_data["EMA_21"].iloc[-1]
    latest_close = price_data["close"].iloc[-1]
    latest_volume = price_data["VOLUME"].iloc[-1]

    # === DIP ===
    if latest_rsi < 30 and latest_close < latest_ema and latest_volume < price_data["VOLUME"].mean():
        return "dip"

    # === BREAKOUT ===
    if latest_rsi > 50 and latest_close > latest_ema and latest_volume > price_data["VOLUME"].mean() * 1.5:
        return "breakout"

    # === SIDEWAYS ===
    return "sideways"
