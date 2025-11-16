# Configuration Guide - AI Trading Assistant

## Overview

The AI Trading Assistant is **configurational** - you can use it standalone or with the autonomous bot. It works effectively on its own, pulling Jupiter perps data directly.

## Quick Start

### 1. Configure Settings

Run the interactive setup:

```bash
python ai_assistant_config.py
```

Or edit `ai_assistant_config.json` directly.

### 2. Choose Your Mode

#### Standalone Mode (Recommended for Manual Trading)

**Use when:**
- Trading on Jupiter (desktop/phone) manually
- Don't want autonomous bot running
- Want AI recommendations without bot infrastructure

**Setup:**
```bash
python ai_assistant_config.py
# Select option 1: Standalone mode
```

**What it does:**
- Pulls Jupiter perps data directly from Jupiter API
- Works completely standalone - no bot needed
- Provides AI recommendations based on Jupiter market data
- Effective scanning/analysis on its own

#### Integrated Mode

**Use when:**
- Want AI recommendations during autonomous bot cycles
- Want to combine AI + bot signals
- Bot infrastructure is available

**Setup:**
```bash
python ai_assistant_config.py
# Select option 2: Integrated mode
```

**What it does:**
- Shows AI recommendations during bot trading cycles
- Uses bot's portfolio and trade history for context
- Combines AI + bot signals

#### Autonomous Bot (Optional)

**Enable only if you want the bot to trade automatically:**

```bash
python ai_assistant_config.py
# Select option 2: Integrated mode
# Then enable autonomous bot when prompted
```

**⚠️ WARNING:** Enabling autonomous bot allows the bot to execute trades automatically!

## Configuration File

`ai_assistant_config.json`:

```json
{
  "autonomous_bot_enabled": false,
  "bot_auto_trade": false,
  "ai_assistant_enabled": true,
  "ai_auto_refresh": false,
  "ai_refresh_interval": 60,
  "primary_data_source": "jupiter",
  "use_jupiter_perps": true,
  "use_bot_data": false,
  "standalone_mode": true,
  "integrate_with_bot": false
}
```

## Usage Scenarios

### Scenario 1: Desktop Trading (Standalone)

You're trading ETH perps on Jupiter on your desktop:

1. **Set standalone mode:**
   ```bash
   python ai_assistant_config.py
   # Select option 1
   ```

2. **Run AI assistant:**
   ```bash
   python seamless_trading_assistant.py
   # Get recommendations while trading manually
   ```

3. **Trade on Jupiter:**
   - Open Jupiter in browser
   - Get AI recommendations from terminal
   - Make trading decisions manually

**No autonomous bot needed!** Works completely standalone.

### Scenario 2: Phone Trading (Standalone)

Trading on your phone while AI assistant runs on desktop:

1. **Desktop: Run AI assistant:**
   ```bash
   python seamless_trading_assistant.py
   # Select option 3: Start auto-refresh
   ```

2. **Phone: Trade on Jupiter**
   - Check AI recommendations on desktop
   - Make trades on Jupiter app/website

**No autonomous bot - just AI recommendations!**

### Scenario 3: With Autonomous Bot

Want bot to run AND get AI recommendations:

1. **Set integrated mode:**
   ```bash
   python ai_assistant_config.py
   # Select option 2
   ```

2. **Enable autonomous bot (optional):**
   ```bash
   python ai_assistant_config.py
   # Enable autonomous bot when prompted
   ```

3. **Run main bot:**
   ```bash
   python main.py
   # AI recommendations appear during cycles
   ```

## Standalone Features

Even in standalone mode, the AI assistant:

✅ **Pulls Jupiter data directly** - No bot needed
✅ **Effective scanning** - Jupiter API for market data
✅ **Comprehensive analysis** - Jupiter insights + sentiment
✅ **Fast recommendations** - 5-10 seconds via Ollama cloud
✅ **Works anywhere** - Desktop, phone, any device with Jupiter

## Configuration Options

### Autonomous Bot Settings

- `autonomous_bot_enabled`: Enable/disable autonomous trading bot
- `bot_auto_trade`: Allow bot to execute trades automatically

### AI Assistant Settings

- `ai_assistant_enabled`: Enable AI assistant (works standalone)
- `ai_auto_refresh`: Auto-refresh recommendations
- `ai_refresh_interval`: Seconds between refreshes

### Data Source Settings

- `primary_data_source`: "jupiter" (recommended)
- `use_jupiter_perps`: Pull directly from Jupiter API
- `use_bot_data`: Use bot's market data (only if integrated)

### Mode Settings

- `standalone_mode`: Works without bot infrastructure
- `integrate_with_bot`: Show recommendations in bot cycles

## Environment Variables

Set these for Ollama cloud:

```bash
# Windows PowerShell
$env:OLLAMA_URL="https://your-ollama-cloud-url.com"
$env:OLLAMA_MODEL="llama3.2"

# Or in .env file
OLLAMA_URL=https://your-ollama-cloud-url.com
OLLAMA_MODEL=llama3.2
```

## Default Behavior

**By default:**
- ✅ Standalone mode (works without bot)
- ✅ Jupiter perps data (primary source)
- ❌ Autonomous bot disabled (manual trading only)
- ✅ AI assistant enabled

**This means you can:**
- Trade manually on Jupiter (desktop/phone)
- Get AI recommendations without bot
- No autonomous trading enabled

## Switching Modes

### Enable Standalone Mode

```python
from ai_assistant_config import get_config
config = get_config()
config.enable_standalone_mode()
```

### Enable Integrated Mode

```python
config.enable_integrated_mode()
```

### Disable Autonomous Bot

```python
config.disable_autonomous_bot()
```

## Best Practices

1. **For manual trading:** Use standalone mode
2. **For bot trading:** Use integrated mode
3. **Never enable autonomous bot** unless you understand the risks
4. **Always test in DRY_RUN mode** first
5. **Use Jupiter as primary source** (most accurate for Jupiter perps)

## Troubleshooting

### "Bot components unavailable"

This is **normal** in standalone mode! The AI assistant works without bot infrastructure.

### "Jupiter data unavailable"

Check your internet connection and Jupiter API status.

### "No portfolio data"

This is **normal** in standalone mode - portfolio data comes from bot (which isn't running).

## Summary

✅ **Standalone mode** = AI recommendations without bot (for manual trading)
✅ **Jupiter API** = Primary data source (works standalone)
✅ **Autonomous bot** = Optional (disabled by default)
✅ **Configuration** = Easy to switch modes

You can trade manually on Jupiter (desktop/phone) and get AI recommendations without running the autonomous bot!

