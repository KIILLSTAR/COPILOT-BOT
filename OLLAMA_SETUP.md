# Ollama Trading AI Assistant Setup Guide

This guide will help you set up Ollama with cloud models for your live trading AI assistant.

## What is Ollama?

Ollama is a tool that lets you run large language models (LLMs) locally or in the cloud. It's perfect for trading assistants because:
- Fast responses for real-time trading decisions
- Works offline (with local models) or in the cloud
- Privacy-focused (your trading data stays private)
- Free and open-source

## Setup Steps

### 1. Install Ollama

**Windows:**
- Download from https://ollama.com/download
- Run the installer
- Ollama will start automatically

**Mac/Linux:**
```bash
curl https://ollama.com/install.sh | sh
```

### 2. Pull a Model

After installation, pull a model. Recommended models for trading:

```bash
# Llama 3.2 (Good balance of speed and intelligence)
ollama pull llama3.2

# Or try Mistral (Fast and efficient)
ollama pull mistral

# Or Qwen (Great for analysis)
ollama pull qwen2.5
```

### 3. Test the Setup

Run the test script:

```bash
python ollama_client.py
```

This will:
- Check if Ollama is running
- List available models
- Test a simple chat

### 4. Configure for Cloud (Optional)

If you want to use a cloud-hosted Ollama instance:

1. Update the `base_url` in `trading_ai_assistant.py`:
```python
assistant = TradingAIAssistant(
    ollama_url="https://your-cloud-ollama-url.com",
    model_name="llama3.2"
)
```

## Using the Trading AI Assistant

### Basic Usage

```python
from trading_ai_assistant import TradingAIAssistant

# Initialize assistant
assistant = TradingAIAssistant(
    ollama_url="http://localhost:11434",
    model_name="llama3.2"
)

# Analyze screen data
screen_data = {
    "price": 3500.0,
    "indicators": {"rsi": 45.0, "ema_12": 3480.0},
    "balance": 10000.0
}

result = assistant.analyze_screen_data(screen_data)
print(result['recommendation'])
print(result['full_analysis'])
```

### Quick Recommendations

For fast decision-making during active trading:

```python
quick_rec = assistant.get_quick_recommendation(
    price=3500.0,
    indicators={"rsi": 45.0, "ema_trend": "bullish"}
)
print(quick_rec)
```

### Live Data Analysis

```python
market_data = {
    "price": 3500.0,
    "rsi": 45.0,
    "volume": 1500000.0,
    "funding_rate": 0.001
}

portfolio = {
    "balance": 10000.0,
    "total_pnl": 100.0,
    "open_positions": 0
}

result = assistant.analyze_live_data(market_data, portfolio)
```

## Comet ML Integration (Optional)

To track experiments and recommendations with Comet:

1. Install Comet ML:
```bash
pip install comet-ml
```

2. Set up Comet account:
   - Sign up at https://www.comet.com
   - Get your API key from settings

3. Set environment variable:
```bash
export COMET_API_KEY="your-api-key-here"
```

4. Enable in assistant:
```python
assistant = TradingAIAssistant(
    ollama_url="http://localhost:11434",
    model_name="llama3.2",
    enable_comet=True
)
```

## Integration with Your Trading Bot

To integrate with your existing trading system:

```python
# In your main trading loop
from trading_ai_assistant import TradingAIAssistant

assistant = TradingAIAssistant()

# Get market data from your sources
market_data = get_market_data()
portfolio = get_portfolio_status()

# Get AI recommendation
ai_result = assistant.analyze_live_data(market_data, portfolio)

# Use recommendation in your trading logic
recommendation = ai_result['recommendation']
if recommendation['action'] == 'LONG' and recommendation['confidence'] >= 7:
    # Consider opening long position
    pass
```

## Troubleshooting

### "Connection failed"
- Make sure Ollama is running: `ollama serve`
- Check if port 11434 is accessible
- For cloud: verify the URL is correct

### "No models found"
- Pull a model: `ollama pull llama3.2`
- Check available models: `ollama list`

### Slow responses
- Use a smaller model (e.g., `mistral` instead of `llama3.2`)
- Check your internet connection (for cloud models)
- Close other applications to free up resources

### Model not found
- List models: `ollama list`
- Pull the model you need: `ollama pull <model-name>`

## Next Steps

1. Run the demo: `python trading_ai_assistant.py`
2. Integrate with your trading bot
3. Experiment with different models
4. Set up Comet ML for tracking (optional)
5. Customize prompts for your trading style

## Model Recommendations for Trading

- **llama3.2**: Good balance, fast, good analysis
- **mistral**: Very fast, good for quick decisions
- **qwen2.5**: Excellent for detailed analysis
- **llama3.1**: More capable but slower

Choose based on your needs:
- Speed priority → `mistral`
- Analysis quality → `qwen2.5`
- Balanced → `llama3.2`

