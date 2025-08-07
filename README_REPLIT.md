# 🚀 ETH Trading Bot - Replit Deployment

## 📱 Mobile-Optimized Trading Bot

This ETH perpetuals trading bot is optimized for mobile devices and can be deployed on Replit for easy access from anywhere.

## 🎯 Features

- **Mobile-Friendly**: Works perfectly on mobile devices
- **Offline Mode**: Simulated trading without internet dependency
- **Real-time Signals**: Technical analysis with RSI, moving averages, momentum
- **Risk Management**: Automatic stop-loss and take-profit
- **Dry Run Mode**: Safe simulation with no real money

## 🚀 Quick Start on Replit

### 1. Fork to Replit
1. Go to [replit.com](https://replit.com)
2. Click "Create Repl"
3. Choose "Import from GitHub"
4. Enter your repository URL
5. Select "Python" as the language

### 2. Run the Bot
- **Offline Version** (Recommended for mobile): Click "Run" - it will execute `main_offline.py`
- **Mobile Version**: Change the run command to `python main_mobile.py`
- **Full Version**: Change the run command to `python main.py`

### 3. Mobile Access
- Open Replit on your mobile browser
- The bot will run in the cloud
- Access from anywhere, anytime
- No need to keep your device running

## 📊 Bot Modes

### 🧪 Offline Mode (`main_offline.py`)
```
✅ No internet required
✅ Fast startup
✅ Realistic ETH price simulation
✅ Technical analysis signals
✅ 15-second cycles
✅ Perfect for mobile
```

### 📱 Mobile Mode (`main_mobile.py`)
```
✅ Reduced API calls
✅ Increased timeouts
✅ 30-second cycles
⚠️ Requires internet
```

### 🔥 Full Mode (`main.py`)
```
✅ All features
✅ Real market data
⚠️ Requires stable internet
⚠️ May stall on mobile networks
```

## 🎮 Controls

- **Start**: Click "Run" button
- **Stop**: Press `Ctrl+C` in the console
- **Restart**: Click "Run" again

## 📈 Trading Strategy

The bot uses multiple technical indicators:

1. **Moving Average Crossover**: 5-period vs 10-period SMA
2. **RSI (Relative Strength Index)**: Oversold/overbought conditions
3. **Momentum Analysis**: Price change over time
4. **Risk Management**: 2% take-profit, 1% stop-loss

## 💰 Simulation Features

- **Starting Balance**: $10,000
- **Trade Size**: $100 per trade
- **Leverage**: 1x (no leverage in simulation)
- **Fees**: Simulated trading fees
- **Funding**: Simulated funding rates

## 🔧 Configuration

### Offline Mode Settings
```python
# In main_offline.py
self.volatility = 0.02  # 2% volatility
self.trend = 0.001      # Slight upward trend
trade_size = 100        # $100 per trade
```

### Mobile Mode Settings
```python
# In main_mobile.py
timeout = 10            # API timeout
cycle_delay = 30        # 30-second cycles
```

## 📱 Mobile Usage Tips

1. **Use Landscape Mode**: Better console visibility
2. **Bookmark the Repl**: Easy access from mobile
3. **Check Console**: Monitor bot activity
4. **Use Offline Mode**: Most reliable on mobile

## 🛡️ Safety Features

- **Dry Run Only**: No real money trading
- **Safety Locks**: Multiple protection layers
- **Simulation Engine**: Realistic but safe trading
- **Error Handling**: Graceful failure recovery

## 🔍 Monitoring

The bot provides real-time updates:
- Current ETH price
- Portfolio balance
- Open positions
- Trading signals
- PnL tracking

## 🚨 Troubleshooting

### Bot Won't Start
1. Check the run command in `.replit`
2. Ensure all dependencies are installed
3. Try the offline version first

### Mobile Issues
1. Use offline mode (`main_offline.py`)
2. Check mobile browser compatibility
3. Try landscape orientation

### Network Issues
1. Switch to offline mode
2. Check internet connection
3. Try mobile mode with longer timeouts

## 📞 Support

- **Issues**: Check the console output
- **Questions**: Review the code comments
- **Mobile Help**: Use offline mode for best results

## 🎉 Ready to Trade!

Your ETH trading bot is now ready to run on Replit and accessible from any mobile device. Start with the offline mode for the best mobile experience!

---

**Remember**: This is a simulation bot for educational purposes. No real money is used.