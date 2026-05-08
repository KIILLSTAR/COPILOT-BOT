# Trading Strategy — COPILOT-BOT

## Signal Generation

Signals combine 5 indicators into a weighted confidence score.
A trade opens when the score reaches the threshold (default: 0.65).

### Indicator Weights

| Indicator | Long Weight | Short Weight | Condition |
|-----------|------------|-------------|-----------|
| RSI(14) | +0.25 | +0.25 | <35 long / >65 short |
| EMA 9/21 | +0.20 | +0.20 | 9>21 long / 9<21 short |
| Bollinger %B | +0.20 | +0.20 | <0.15 long / >0.85 short |
| Funding rate | +0.10 | +0.15 | pos long / neg short |
| OI ratio | +0.10 | +0.10 | short-heavy long / long-heavy short |

**Max possible score: 0.85 long / 0.90 short**

## Risk Management

- Stop Loss: 2% (default)
- Take Profit: 4% (default) — 2:1 RR ratio
- Max 1 open position at a time
- Max 10 trades/day
- Auto-close if balance drawdown > $50

## Market: ETH-PERP on Jupiter Perpetuals (Solana)

Price data sourced from: Jupiter Perps → Binance Futures → CoinGecko
