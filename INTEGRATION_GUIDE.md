# Integration Guide: Ollama Assistant + COPILOT-BOT

This guide shows how the Ollama trading AI assistant integrates with your existing COPILOT-BOT infrastructure.

## What Code is Reused

### ✅ Reused Components

1. **Market Data Fetching** (`ai_signal_detector.py`)
   - Uses `AISignalDetector.get_market_data()` method
   - Gets comprehensive market data (RSI, EMA, Bollinger Bands, funding rates, etc.)
   - Handles errors gracefully with fallbacks

2. **Price Fetching** (`core/price_fetcher.py`)
   - Uses robust `price_fetcher.get_eth_price()` 
   - Multi-source fallbacks (Drift, Jupiter, Binance, CoinGecko)
   - Handles network errors and retries

3. **Portfolio Status** (`core/simulation_engine.py`)
   - Uses `simulator.get_portfolio_summary()`
   - Gets balance, PnL, win rate, open positions
   - Includes trade history

4. **Configuration** (`app_config.py`)
   - Reuses your safety configs and trade configs
   - Respects DRY_RUN mode and safety locks

5. **Logging** (`app_logger.py`)
   - Integrates with your existing logging system
   - Logs AI recommendations to trade log

6. **CLI Patterns** (`app_cli.py`)
   - Similar menu structure and user interaction patterns
   - Familiar interface for your users

## How It Works

### Integration Flow

```
┌─────────────────────────┐
│  Ollama AI Assistant    │
│  (trading_ai_assistant) │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│  Integrated Assistant   │
│ (ollama_trading_        │
│   integration)          │
└────────────┬────────────┘
             │
             ├──► Uses AISignalDetector.get_market_data()
             ├──► Uses simulator.get_portfolio_summary()
             ├──► Uses price_fetcher.get_eth_price()
             └──► Uses app_logger._write_log()
             
┌─────────────────────────┐
│  Your Existing Bot      │
│  (COPILOT-BOT)          │
└─────────────────────────┘
```

### Key Integration Points

1. **Market Data** → Your bot's comprehensive market data → Ollama analysis
2. **Portfolio** → Your simulation engine data → Ollama recommendations  
3. **Trade History** → Your bot's trade history → Context for AI
4. **Configuration** → Your safety/config system → Controls assistant behavior
5. **Logging** → Your logging system → Tracks AI recommendations

## Usage Examples

### Example 1: Quick Recommendation During Trading

```python
from ollama_trading_integration import IntegratedTradingAssistant

assistant = IntegratedTradingAssistant()

# Get fast recommendation using your existing market data
quick_rec = assistant.get_quick_recommendation()
print(quick_rec)
```

### Example 2: Full Analysis

```python
# Get comprehensive analysis with all your bot's data
result = assistant.analyze_and_recommend()

print(f"Action: {result['recommendation']['action']}")
print(f"Confidence: {result['recommendation']['confidence']}/10")
print(f"Analysis: {result['analysis']}")
```

### Example 3: Integration with Main Trading Loop

```python
# In your main.py or trading loop
from ollama_trading_integration import IntegratedTradingAssistant

assistant = IntegratedTradingAssistant()

# In your trading cycle
while True:
    # Your existing signal detection
    signal_result = run_ai_signal_loop(cfg)
    
    # Get AI assistant recommendation
    ai_recommendation = assistant.analyze_and_recommend()
    
    # Combine signals (your logic + AI recommendation)
    if signal_result and ai_recommendation['recommendation']['action'] == 'LONG':
        # Consider trade
        pass
```

### Example 4: CLI Usage

```bash
# Run the integrated CLI
python ollama_trading_integration.py

# Or use it interactively
python -c "from ollama_trading_integration import integrated_cli_menu; integrated_cli_menu()"
```

## Benefits of Integration

### ✅ No Duplication
- Reuses your existing market data fetching
- Uses your portfolio tracking
- Leverages your error handling

### ✅ Consistent Data
- Same data sources as your bot
- Same price feeds
- Same portfolio calculations

### ✅ Unified Logging
- AI recommendations logged with your trades
- Consistent audit trail
- Easy to track performance

### ✅ Safety Integration
- Respects your safety configs
- Works with DRY_RUN mode
- Honors safety locks

## Standalone Mode

If you want to use the Ollama assistant without your full bot:

```python
# Works standalone with basic market data
from trading_ai_assistant import TradingAIAssistant

assistant = TradingAIAssistant()

# Provide your own market data
market_data = {
    "price": 3500.0,
    "rsi": 45.0,
    "volume": 1500000.0
}

result = assistant.analyze_screen_data(market_data)
```

## Configuration

The integration respects your existing configuration:

- **DRY_RUN mode**: Assistant knows if you're in simulation
- **Safety locks**: Honors your safety settings
- **Logging**: Uses your log file locations
- **Trading configs**: Respects your trade size, leverage, etc.

## Next Steps

1. **Test Integration**: Run `python ollama_trading_integration.py`
2. **Try CLI**: Use the interactive menu to explore features
3. **Integrate with Bot**: Add to your main trading loop
4. **Customize**: Adjust prompts in `trading_ai_assistant.py` for your style
5. **Track Performance**: Enable Comet ML for recommendation tracking

## Troubleshooting

### "Import errors"
- Make sure you're in the COPILOT-BOT directory
- Check that your existing bot components are available

### "Market data unavailable"
- The integration has fallbacks
- Will use basic data if your bot components aren't available
- Check your network connection for price feeds

### "Portfolio data empty"
- If simulator isn't initialized, uses default values
- Make sure your simulation engine is set up
- Check `simulation_data.json` exists

## Customization

### Modify AI Prompts

Edit `trading_ai_assistant.py` to customize:
- Analysis style
- Recommendation format
- Risk assessment approach

### Add Data Sources

The integration can easily be extended to include:
- Additional market indicators
- Alternative data sources
- Custom portfolio metrics

### Custom CLI Commands

Extend `ollama_trading_integration.py` to add:
- Custom analysis modes
- Specific market queries
- Historical analysis

## Support

- **Ollama Setup**: See `OLLAMA_SETUP.md`
- **Integration Issues**: Check import paths and dependencies
- **Bot Components**: Verify your existing bot runs correctly first

