# Quick Start - Run the Voice Assistant NOW!

## Step 1: Set Your Ollama Credentials

**Option A: PowerShell (Quick)**
```powershell
$env:OLLAMA_URL="https://api.ollama.ai/v1"
$env:OLLAMA_API_KEY="paste-your-api-key-here"
```

**Option B: Edit .env File**
1. Open: `C:\Users\natha\OneDrive\Desktop\COPILOT REPO\COPILOT-BOT\.env`
2. Add:
   ```
   OLLAMA_URL=https://api.ollama.ai/v1
   OLLAMA_API_KEY=your-api-key-here
   OLLAMA_MODEL=llama3.2
   ```
3. Save

## Step 2: Run the Voice Assistant!

```powershell
python voice_assistant.py
```

## That's It! 🚀

The assistant will:
1. ✅ Load your credentials from .env or environment
2. ✅ Connect to Ollama cloud
3. ✅ Pull Jupiter perps data
4. ✅ Give you AI recommendations with voice!

## Quick Commands Once Running

- **"analyze"** - Full AI recommendation
- **"quick"** - Brief recommendation
- **"status"** - Current price and sentiment
- **"exit"** - Exit voice mode

## If You Have Issues

1. **Test connection first:**
   ```powershell
   python test_ollama_connection.py
   ```

2. **Check credentials:**
   - Make sure OLLAMA_URL is set
   - Make sure OLLAMA_API_KEY is set
   - No extra spaces in keys

3. **Try text-only mode:**
   ```powershell
   python seamless_trading_assistant.py
   ```

## Ready to Run?

Just set your credentials (Step 1) and run:
```powershell
python voice_assistant.py
```

Good luck! 🎉

