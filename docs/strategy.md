# Strategy: ETH Perps Bot

## Indicators Used
- RSI (14)
- EMA Fast (9)
- EMA Slow (21)
- Volume Spike (> 1.5x 20-period average)

## Signal Logic
- BUY: RSI < 30 and EMA Fast > EMA Slow and Volume Spike
- SELL: RSI > 70 and EMA Fast < EMA Slow
- HOLD: Otherwise

## Future Ideas
- Add MACD or Bollinger Bands
- Multi-asset support (SOL, meme coins)
- Dynamic position sizing
- Telegram alerts
