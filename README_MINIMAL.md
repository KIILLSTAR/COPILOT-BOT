# 🛡️ Jupiter ETH Perps Bot - Minimal & Safe

A **clean, minimalistic trading bot** with **multiple safety layers** to protect your funds during development and testing.

## 🚀 Quick Start

```bash
# 1. Install dependencies
pip install --break-system-packages requests solana base58

# 2. Verify safety (IMPORTANT!)
python3 test_safety.py

# 3. Start the minimal interface
python3 main_minimal.py
```

## 💚 Safety First

**Your funds are 100% protected** by multiple safety layers:

- 🔒 **Primary Safety Lock** - Hard-coded protection
- 🌍 **Environment Variable** - Must be explicitly enabled
- 📁 **Manual Confirmation File** - Must exist for live trading  
- 💳 **Wallet Approval** - Double confirmation required

**Result: DRY RUN mode is FORCED** - no real money can be lost!

## 🎮 Minimal Interface

```
┌─────────────────────────────────────────────────────────────┐
│ 🛡️ ETH PERPS BOT │ 🔒 SAFE DRY RUN │ MANUAL  │ 14:32:15 │
└─────────────────────────────────────────────────────────────┘
  🔒 SAFETY ACTIVE - YOUR FUNDS ARE PROTECTED
  Balance: $10,000  │  PnL: +$245  │  Trades: 8

Commands:
  [s] Start/Stop bot
  [a] Toggle auto-approve
  [t] Show transactions
  [h] Help
  [x] Safety status
  [q] Quit
```

### Features

- **One-letter commands** - Simple navigation
- **Expandable menus** - Only see what you need
- **Real-time updates** - Live portfolio tracking
- **Trade approval** - Manual or auto mode
- **Safety status** - Always visible protection

## 📊 What You Get

### Dry Run Simulation
- **Real market data** from multiple sources
- **Realistic fees** and slippage calculation
- **Funding costs** simulation
- **Stop loss/take profit** execution
- **Complete trade history** tracking

### Smart Trading
- **Technical analysis** (RSI, EMA, Bollinger Bands)
- **Cross-exchange arbitrage** detection
- **Funding rate analysis** 
- **Market sentiment** evaluation

## 🧪 Testing Your Strategy

1. **Start the bot**: `python3 main_minimal.py`
2. **Press 's'** to start trading simulation
3. **Watch it trade** with real market data
4. **Check results** by pressing 't' for transactions

All trades are **100% simulated** - no real money involved!

## 📈 Understanding Results

The bot tracks everything:
- **Win Rate** - Percentage of profitable trades
- **PnL** - Total profit/loss from all trades
- **Largest Win/Loss** - Best and worst trades
- **Fees Paid** - Realistic trading costs
- **ROI** - Return on investment percentage

## 🔧 Customization

Edit `config/trade_config.py`:
```python
TRADE_SIZE_USD = 100        # Trade size per position
LEVERAGE = 1.0              # Leverage multiplier  
STOP_LOSS_PCT = 0.02        # 2% stop loss
TAKE_PROFIT_PCT = 0.04      # 4% take profit
CYCLE_DELAY_SECONDS = 60    # Time between trades
```

## ⚠️ Want Live Trading?

**NOT RECOMMENDED** for beginners, but if you must:

1. Edit `config/safety_config.py` - set `SAFETY_LOCK_ENABLED = False`
2. Set environment: `ENABLE_LIVE_TRADING=TRUE`  
3. Create file: `.live_trading_confirmed`
4. Set environment: `WALLET_APPROVED_LIVE_TRADING=TRUE`
5. Add your wallet private key to `.env`

**ALL 4 steps required** - any missing step forces dry run mode.

## 📁 Project Structure

```
├── main_minimal.py          # Main entry point
├── test_safety.py           # Safety verification 
├── config/
│   ├── safety_config.py     # 🔒 Safety protection
│   └── trade_config.py      # Trading parameters
├── dashboard/
│   └── minimal_dashboard.py # Clean interface
├── core/
│   ├── simulation_engine.py # Dry run engine
│   └── indicators.py        # Technical analysis
└── strategy/
    └── signal_detector.py   # Trading logic
```

## 💡 Tips

- **Start with dry run** - Test your strategy first
- **Monitor win rate** - Aim for >60% for profitability  
- **Check max drawdown** - Ensure you can handle losses
- **Use small sizes** - Even in live trading, start small
- **Safety first** - Keep protection layers active

---

**🛡️ Your funds are protected. Happy testing!**