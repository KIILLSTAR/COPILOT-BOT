# COPILOT-BOT 🤖

Autonomous ETH-PERP trading bot running on Jupiter Perpetuals (Solana).
Currently in **dry run mode** — all trades are simulated, no real money moves.

## Architecture

```
copilot-bot/
├── main.py                   # Single entry point
├── config/
│   ├── trade_config.py       # All tunable parameters
│   └── safety_config.py      # Safety locks & dry run enforcement
├── core/
│   ├── bot_engine.py         # Main loop orchestrator
│   ├── jupiter_perps.py      # Jupiter Perpetuals API client
│   ├── price_fetcher.py      # Price feed (Jupiter → Binance → CoinGecko)
│   ├── simulation_engine.py  # Dry run position manager
│   └── indicators.py         # RSI, EMA, Bollinger Band calculations
├── strategy/
│   └── signal_detector.py    # Signal generation (RSI + EMA + BB + funding + OI)
├── dashboard/
│   ├── app.py                # Flask web dashboard (mobile-optimized)
│   └── templates/            # HTML templates
└── wallet/
    ├── secure_wallet.py      # Wallet management (live trading only)
    └── trade_executer.py     # Trade execution (live trading only)
```

## How to Run

```bash
pip install -r requirements.txt

python main.py          # bot + dashboard (default)
python main.py --web    # dashboard only
python main.py --bot    # bot only
```

Dashboard runs at `http://localhost:5000`

## Strategy

Signals are generated from 5 indicators:
- **RSI(14)** — oversold/overbought detection
- **EMA 9/21 crossover** — trend direction
- **Bollinger Bands(20)** — price extremes
- **Funding rate** — Jupiter perp market sentiment
- **OI ratio** — long/short open interest imbalance

A signal fires when combined confidence score ≥ 0.65.

## Configuration

All parameters in `config/trade_config.py`:
- `TRADING_PAIR` — default: ETH-PERP
- `TRADE_SIZE_USD` — default: $100
- `LEVERAGE` — default: 2x
- `STOP_LOSS_PCT` — default: 2%
- `TAKE_PROFIT_PCT` — default: 4%
- `SIGNAL_THRESHOLD` — default: 0.65

## Safety

- `DRY_RUN = True` is **hardcoded** — cannot accidentally trade real money
- Live trading requires explicit env var unlock (`ENABLE_LIVE_TRADING=TRUE`)
- Max daily trades: 10
- Auto-close if total loss exceeds $50

## Status

🟢 Bot logic running autonomously on Base44 cloud (every 15 min)
🟡 Live trading: NOT enabled
