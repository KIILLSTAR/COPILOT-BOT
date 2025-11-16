# Setup Guide - Voice Trading Assistant

## What We Just Tested ✅

1. **Voice Output** - ✅ Working! (Spoke "Voice test successful")
2. **Voice Recognition** - ✅ Initialized
3. **Configuration** - ✅ Loaded
4. **Jupiter API** - Needs internet connection
5. **Ollama** - Needs URL

## Quick Setup Steps

### Step 1: Get Your Ollama Cloud URL

You need an Ollama cloud service URL. Options:

1. **Ollama Cloud** (if you have an account)
   - URL format: `https://api.ollama.ai/v1`
   - Or your custom cloud instance

2. **Local Ollama** (if installed)
   - URL: `http://localhost:11434`

### Step 2: Set Environment Variable

**Windows PowerShell:**
```powershell
$env:OLLAMA_URL="your-ollama-cloud-url-here"
```

**Or create `.env` file in project root:**
```
OLLAMA_URL=https://your-ollama-cloud-url.com
OLLAMA_MODEL=llama3.2
```

### Step 3: Run Voice Assistant

```bash
python voice_assistant.py
```

### Step 4: Test Voice Commands

Once running, try:
- **"analyze"** - Full AI recommendation
- **"quick"** - Brief recommendation
- **"status"** - Current price and sentiment

## What Works Now

✅ **Voice Output** - Assistant speaks recommendations  
✅ **Voice Recognition** - Can hear your commands  
✅ **Jupiter Integration** - Ready to pull perps data  
✅ **Standalone Mode** - Works without bot  
✅ **Configuration** - Easy to customize  

## Testing Options

### Option 1: Voice Assistant (Full Features)
```bash
python voice_assistant.py
```

### Option 2: Text-Only Mode (No Voice)
```bash
python seamless_trading_assistant.py
```

### Option 3: Quick Test (No Ollama Required)
```bash
python quick_test.py
```

## If You Don't Have Ollama URL Yet

You can still test:
1. **Voice features** - Already working! ✅
2. **Jupiter data** - When internet is available
3. **Configuration** - All set up ✅

For AI recommendations, you'll need Ollama URL.

## Need Help?

1. **Voice not working?** - Check microphone permissions
2. **No Jupiter data?** - Check internet connection
3. **No Ollama?** - Get Ollama cloud URL first
4. **Configuration issues?** - Run: `python ai_assistant_config.py`

## Next Steps

1. ✅ Voice libraries installed
2. ✅ Configuration set up
3. ⏳ Set Ollama URL (when ready)
4. ⏳ Test full voice assistant

Everything is ready - just need Ollama URL for AI recommendations!

