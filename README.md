# 🤖 COPILOT BOT — Jupiter ETH Perpetuals Trading Bot

A clean, consolidated autonomous trading bot for Jupiter Perpetuals on Solana.
Built for dry-run simulation first, live trading when you're ready.

## 🚀 Quick Start

```bash
pip install -r requirements.txt
python main.py         # bot + dashboard (recommended)
python main.py --web   # dashboard only
python main.py --bot   # bot engine only
```

Dashboard runs at: `http://localhost:5000`

## 🏗️ Project Structure

```
copilot-bot/
├── main.py                    ← Single entry point
├── requirements.txt
├── .env.example
├── config/
│   ├── trade_config.py        ← All trading parameters
│   └── safety_config.py       ← Safety locks (read before touching)
├── core/
│   ├── jupiter_perps.py       ← Jupiter Perps API client
│   ├── price_fetcher.py       ← Multi-source price feed
│   ├── simulation_engine.py   ← Dry run engine
│   └── bot_engine.py          ← Main trading loop
├── strategy/
│   └── signal_detector.py     ← RSI + EMA + BB + funding + OI signals
├── dashboard/
│   └── app.py                 ← Flask web dashboard
└── data/                      ← Auto-created: logs, state, price cache
```

## 🔒 Safety

Dry run is **hardcoded ON** by default. Four locks must all be disabled to enable live trading. You will not accidentally trade real money.

## 📊 Signals Used

- RSI (14) — oversold/overbought
- EMA 9/21 crossover — trend direction
- Bollinger Bands — price extremes
- Jupiter funding rate — market bias
- Open interest ratio — long/short imbalance

## 🌐 Dashboard Features

- Real-time ETH price from Jupiter Perps API
- Signal direction + confidence score
- Open positions with unrealized PnL
- Trade history with realized PnL
- All market indicators in one view
- Mobile-optimized dark theme
