# 🛡️ Jupiter ETH Perps Trading Bot - Safe & Minimal

**A clean, professional trading bot with multiple safety layers to protect your funds.**

Built for learning, testing, and eventually scaling to live trading with complete confidence.

## 🚀 Quick Start (Recommended)

```bash
# 1. Install core dependencies
pip install --break-system-packages requests solana base58

# 2. IMPORTANT: Verify all safety systems are working
python3 test_safety.py

# 3. Start the minimal, clean interface
python3 main_minimal.py
```

That's it! Your funds are 100% protected by multiple safety layers.

---

## 💚 Safety First - Your Funds Are Protected

**🛡️ FOUR LAYERS OF PROTECTION:**

1. **🔒 Primary Safety Lock** - Hard-coded in `config/safety_config.py`
2. **🌍 Environment Variable** - `ENABLE_LIVE_TRADING` must be explicitly set  
3. **📁 Manual Confirmation** - `.live_trading_confirmed` file must exist
4. **💳 Wallet Approval** - `WALLET_APPROVED_LIVE_TRADING` environment variable

**Result: DRY RUN MODE IS FORCED** - No real money can ever be lost during development!

---

## 🎮 What You'll See

### Minimal, Clean Interface
```
┌─────────────────────────────────────────────────────────────┐
│ 🛡️ ETH PERPS BOT │ 🔒 SAFE DRY RUN │ MANUAL  │ 14:32:15 │
└─────────────────────────────────────────────────────────────┘
  🔒 SAFETY ACTIVE - YOUR FUNDS ARE PROTECTED
  Balance: $10,000  │  PnL: +$245  │  Trades: 8

Commands:
  [s] Start/Stop bot          [h] Help
  [a] Toggle auto-approve     [x] Safety status  
  [t] Show transactions       [q] Quit

Status: Stopped  │  Open Positions: 0
```

### Simple Commands
- **One letter** = one action
- **No complex menus** = easy navigation  
- **Expandable sections** = see only what you need
- **Always safe** = multiple protection layers

---

## 📊 What The Bot Does

### 🧠 Smart Analysis
- **Real-time ETH prices** from multiple sources (CoinGecko, Jupiter, Binance)
- **Technical indicators** (RSI, EMA, Bollinger Bands)  
- **Cross-exchange arbitrage** detection
- **Funding rate analysis** between exchanges
- **Market sentiment** evaluation

### 🎯 Realistic Simulation  
- **Real market data** at exact trade moments
- **Realistic fees** (0.1% trading fees)
- **Funding costs** simulation
- **Stop loss & take profit** automatic execution
- **Complete trade history** with performance metrics

### 📈 Performance Tracking
- **Win Rate** - Percentage of profitable trades
- **PnL** - Total profit/loss tracking
- **ROI** - Return on investment
- **Max Drawdown** - Worst losing streak
- **Fee Analysis** - Total trading costs

---

## 🧪 Test Your Strategy

1. **Start**: `python3 main_minimal.py`
2. **Press 's'** to start the trading bot
3. **Watch it analyze** the market every 60 seconds
4. **Approve trades** manually or switch to auto mode
5. **Check results** with 't' to see your trades

**Everything is simulated** - test with confidence!

---

## ⚙️ Customization

Edit your trading parameters in `config/trade_config.py`:

```python
# Trading Parameters
TRADE_SIZE_USD = 100        # Base trade size in USD
LEVERAGE = 1.0              # Leverage (1x = no leverage)
STOP_LOSS_PCT = 0.02        # 2% stop loss
TAKE_PROFIT_PCT = 0.04      # 4% take profit

# Timing
CYCLE_DELAY_SECONDS = 60    # Seconds between analysis cycles
SIGNAL_THRESHOLD = 0.75     # Minimum confidence to trade

# Risk Management  
MAX_LOSS_THRESHOLD = 50.0   # Max loss before auto-close
AUTO_CLOSE_ENABLED = True   # Enable automatic position closing
```

---

## 🏗️ Project Structure

```
📁 Your Trading Bot
├── 🚀 main_minimal.py          # Start here - main entry point
├── 🔒 test_safety.py           # Verify safety (run first!)
│
├── 📊 config/
│   ├── safety_config.py        # 🛡️ Protection layers (CRITICAL)
│   └── trade_config.py         # ⚙️ Trading parameters
│
├── 🎮 dashboard/
│   └── minimal_dashboard.py    # Clean, simple interface
│
├── 🧠 core/
│   ├── simulation_engine.py    # Dry run trading engine
│   ├── indicators.py           # Technical analysis
│   ├── drift_client.py         # ETH perps data integration
│   └── jupiter_integration.py  # Jupiter ecosystem data
│
├── 📈 strategy/  
│   └── signal_detector.py      # Smart trading logic
│
└── 💳 wallet/
    ├── secure_wallet.py        # Secure wallet management
    └── TOKEN_config.py          # Token configurations
```

---

## 🎯 For Beginners

### First Time Using?
1. **Run safety test**: `python3 test_safety.py` ✅
2. **Start bot**: `python3 main_minimal.py` 🚀  
3. **Press 'h'** to see help menu 📖
4. **Press 's'** to start trading simulation 🎮

### Understanding Results
- **Green numbers** = Profit 💚
- **Red numbers** = Loss ❤️  
- **Win Rate > 60%** = Good strategy 📈
- **Check 't' menu** = See all your trades 📊

### Next Steps
1. **Test different parameters** in `config/trade_config.py`
2. **Run for several hours** to see strategy performance
3. **Analyze results** - aim for consistent profitability
4. **Only consider live trading** after extensive testing

---

## 🔧 Advanced Setup (Optional)

### Full Setup with Environment Variables
```bash
# 1. Copy environment template
cp .env.example .env

# 2. Edit .env with your settings (optional for dry run)
nano .env

# 3. Run full setup
python3 setup.py
```

### Alternative Interfaces
```bash
# Original comprehensive interface
python3 main.py

# Dashboard-only demo
python3 demo_minimal.py

# Dry run testing
python3 test_dry_run.py
```

---

## ⚠️ Want Live Trading Eventually?

**STOP! Not recommended until you:**
- ✅ Have tested for weeks in dry run
- ✅ Have consistent 60%+ win rate  
- ✅ Understand all risks involved
- ✅ Can afford to lose the money

**If you still want to proceed:**
1. Edit `config/safety_config.py` → `SAFETY_LOCK_ENABLED = False`
2. Set environment: `export ENABLE_LIVE_TRADING=TRUE`
3. Create file: `touch .live_trading_confirmed`  
4. Set environment: `export WALLET_APPROVED_LIVE_TRADING=TRUE`
5. Add real wallet private key to `.env`

**ALL 5 steps required** - missing any step = forced dry run mode.

---

## 🆘 Troubleshooting

### Bot Won't Start?
```bash
# Check dependencies
python3 -c "import requests, solana, base58; print('✅ All good')"

# Verify safety
python3 test_safety.py
```

### Want to Reset Simulation?
```bash
# Delete simulation data
rm simulation_data.json

# Restart with fresh $10,000
python3 main_minimal.py
```

### Need Help?
- Press **'h'** in the bot for help menu
- Press **'x'** to see detailed safety status
- Check `test_safety.py` output for diagnostics

---

## 📋 What's Included

- ✅ **Safe dry run simulation** with real market data
- ✅ **Minimal, clean interface** - easy to navigate
- ✅ **Technical analysis** - RSI, EMA, Bollinger Bands
- ✅ **Risk management** - Stop loss, take profit, position sizing  
- ✅ **Performance tracking** - Win rate, PnL, trade history
- ✅ **Multi-source data** - CoinGecko, Jupiter, Binance integration
- ✅ **Trade approval system** - Manual or automatic
- ✅ **Complete protection** - Multiple safety layers
- ✅ **Easy customization** - Simple config files

---

## 🎉 Ready to Start!

Your trading bot is **ready to use safely**. All protection mechanisms are active.

```bash
# 🛡️ Verify everything is safe
python3 test_safety.py

# 🚀 Start trading (safely!)
python3 main_minimal.py
```

**Happy (safe) trading! 🛡️💚**
