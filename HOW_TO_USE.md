# How to Use the AI Trading Assistant

## Current Setup Explained

### ❌ What You DON'T Need
- **Comet's interface** - Comet ML is optional for experiment tracking only, not the interface
- **Ollama's application** - Ollama cloud runs in the background via API calls
- **Separate terminal windows** - Can be integrated into your main bot

### ✅ What You Actually Use

Right now you have **two options**:

## Option 1: Standalone CLI Script (Current)

Run separately when you want AI recommendations:

```bash
python seamless_trading_assistant.py
```

**When to use:**
- Quick check before trading
- Manual analysis when you're not actively trading
- Testing AI recommendations

**Workflow:**
1. Open terminal
2. Run the script
3. Select option 1 for analysis
4. Get recommendation
5. Go to Jupiter and trade manually

## Option 2: Integrated into Your Trading Bot (RECOMMENDED)

AI recommendations appear automatically during your trading cycles:

```bash
python main_with_ai_assistant.py
```

**When to use:**
- During active trading sessions
- Want AI recommendations alongside your bot's signals
- Trading on Jupiter in real-time

**Workflow:**
1. Run `main_with_ai_assistant.py`
2. Bot runs normally
3. **Before each trading cycle**, AI automatically:
   - Gathers Jupiter market data
   - Analyzes with Ollama cloud
   - Shows recommendation
4. Then your bot's signal detection runs
5. You see both signals + AI recommendation
6. Make trading decision on Jupiter

## How It Works During Trading

### Example Output:

```
📊 TRADING CYCLE #1
==================================================

💰 Balance: $10,000.00 | PnL: $50.00 | Open: 1 positions

🤖 Getting AI recommendation...

==================================================
🤖 AI RECOMMENDATION
==================================================
Action: LONG | Confidence: 8/10
Jupiter Price: $3,520.50 | Sentiment: BULLISH
Reasoning: Jupiter shows strong liquidity with low price impact.
EMA crossover indicates bullish trend. High confidence long signal...
==================================================

🔍 Running signal detection...
[Your bot's signal logic here]

📊 Monitoring positions...
```

You get:
1. **AI recommendation** (from Ollama cloud)
2. **Your bot's signal** (existing logic)
3. **Both together** to make decisions on Jupiter

## Setup Steps

### 1. Set Ollama Cloud URL

```bash
# Windows PowerShell
$env:OLLAMA_URL="https://your-ollama-cloud-url.com"

# Or create .env file
OLLAMA_URL=https://your-ollama-cloud-url.com
OLLAMA_MODEL=llama3.2
```

### 2. Choose Your Workflow

**Option A: Standalone (on-demand)**
```bash
python seamless_trading_assistant.py
```

**Option B: Integrated (recommended for active trading)**
```bash
python main_with_ai_assistant.py
```

### 3. Trade on Jupiter

- Open Jupiter in your browser
- See AI recommendations in terminal
- Make trading decisions based on:
  - AI recommendation (confidence score)
  - Your bot's signals
  - Jupiter market data shown

## What You See

### During Each Trading Cycle:

1. **Portfolio Status** (from your simulator)
2. **AI Recommendation** (from Ollama)
   - Action: LONG/SHORT/HOLD
   - Confidence: 1-10
   - Jupiter market data
   - Reasoning
3. **Your Bot's Signals** (existing logic)
4. **Both together** for decision-making

## Advantages

✅ **No clicking** - Everything automatic
✅ **No screen scanning** - All data gathered programmatically  
✅ **Integrated workflow** - Works with your existing bot
✅ **Fast** - 5-10 seconds for AI analysis
✅ **Jupiter-focused** - Primary data from Jupiter ETH perps
✅ **Seamless** - Recommendations appear during trading cycles

## Optional: Comet ML Tracking

If you want to track AI recommendations over time:

1. Install: `pip install comet-ml`
2. Set API key: `$env:COMET_API_KEY="your-key"`
3. Enable in code: `enable_comet=True`

This just tracks data - you don't interact with Comet's interface.

## Future Enhancements

We can add:
- Web dashboard showing live recommendations
- Desktop notifications for high-confidence signals
- Telegram/Discord alerts
- Integration with Jupiter API for auto-trading (with your approval)

## Questions?

**Q: Do I need Comet open?**  
A: No, Comet is just for data tracking (optional)

**Q: Do I need Ollama app?**  
A: No, Ollama cloud runs via API in background

**Q: Can I use it while trading on Jupiter?**  
A: Yes! Run `main_with_ai_assistant.py` and recommendations appear automatically

**Q: Does it trade for me?**  
A: No, it gives recommendations. You make the trades on Jupiter.

