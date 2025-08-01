# 🚀 COPILOT-BOT: ETH Perps Trading Bot

A modular, automated trading bot for ETH perpetuals on Solana using Jupiter Aggregator. Includes CLI and web dashboards for mobile control.

[![Run on Replit](https://replit.com/badge/github/KIILLSTAR/COPILOT-BOT)](https://replit.com/github/KIILLSTAR/COPILOT-BOT)
---

## 📱 Mobile Access

### ✅ iPhone & Android
- Use [Replit](https://replit.com) in browser or app
- Run `main.py` to execute bot
- Run `dashboard.py` for CLI view
- Run `web_dashboard.py` for browser dashboard

# 🧠 Modular Trading Bot (ETH Perpetuals + Solana Spot)

A fully modular, audit-friendly trading bot with manual control, dry-run mode, and mobile-ready dashboard. Built for Replit deployment and real-time experimentation.

---

## 🚀 Quick Start (Replit)

1. **Fork or Upload Repo to Replit**
   - Include: `main.py`, `dashboard.py`, `strategy/`, `wallet/`, `logger/`, `config/`

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt

---
# 🧠 Solana Trading Bot

Modular, mobile-friendly bot for multi-asset trading with audit logging and manual trade confirmation.

## 📦 Folder Structure
- `core/`: Signal detection, Jupiter API, strategy logic
- `wallet/`: SafeWalletManager, logger, token config
- `cli/`: Mode toggler, audit viewer
- `dashboard/`: Flask dashboard
- `utils/`: Dry run, config, setup

## 🧠 Features

- RSI, EMA, Volume Spike strategy
- Dry run mode for safe testing
- Phantom wallet integration
- Trade logging and performance tracking
- CLI dashboard (Rich)
- Web dashboard (Textual)

---

## ⚙️ Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt

# 🔁 Modular Trading Bot with Jupiter Feed + Audit Dashboard

This bot scans live signals from Jupiter (RSI + EMA + volume), lets you confirm trades manually or automatically, and logs every decision for full auditability. Built for mobile-friendly control via Flask dashboard.

---

## 🚀 Features

- ✅ Real-time price feed from Jupiter (`SOL/USDC`, `ETH/USDC`, etc.)
- 📈 Signal engine using RSI, EMA, and volume
- 🔐 SafeWalletManager with manual/auto modes
- 🧾 Audit logging of every trade decision
- 📊 Web dashboard for mobile control
- 🧭 CLI viewer for past trades
