# Setting Up Ollama Cloud

## Quick Setup Guide

You have your **API key** and **device key** from Ollama's website. Here's how to set them up:

## Option 1: Using .env File (Recommended)

1. **Open the .env file** in your project root:
   ```
   C:\Users\natha\OneDrive\Desktop\COPILOT REPO\COPILOT-BOT\.env
   ```

2. **Edit it to add your credentials:**
   ```
   OLLAMA_URL=https://api.ollama.ai/v1
   OLLAMA_API_KEY=your-api-key-here
   OLLAMA_MODEL=llama3.2
   ```

   Replace `your-api-key-here` with your actual API key or device key.

3. **Save the file**

4. **Install python-dotenv** (to load .env automatically):
   ```powershell
   pip install python-dotenv
   ```

5. **Run the assistant:**
   ```powershell
   python voice_assistant.py
   ```

## Option 2: Using PowerShell Environment Variables

**Run these commands in PowerShell:**

```powershell
$env:OLLAMA_URL="https://api.ollama.ai/v1"
$env:OLLAMA_API_KEY="your-api-key-here"
```

Replace `your-api-key-here` with your actual API key or device key.

**Then run:**
```powershell
python voice_assistant.py
```

## Finding Your Ollama URL

The URL format depends on your Ollama cloud provider:

1. **Ollama Cloud** (default): `https://api.ollama.ai/v1`
2. **Custom instance**: Check your Ollama cloud dashboard
3. **Local Ollama**: `http://localhost:11434` (if running locally)

## Using Your Device Key

Your **device key** works the same as the API key. Use either:

- `OLLAMA_API_KEY=your-device-key` or
- `OLLAMA_DEVICE_KEY=your-device-key`

Both work!

## Testing Your Connection

**After setting credentials, test with:**
```powershell
python test_ollama_connection.py
```

Or run the voice assistant directly:
```powershell
python voice_assistant.py
```

## Quick Commands

**1. Set credentials in PowerShell:**
```powershell
$env:OLLAMA_URL="https://api.ollama.ai/v1"
$env:OLLAMA_API_KEY="paste-your-key-here"
```

**2. Run voice assistant:**
```powershell
python voice_assistant.py
```

**3. Test connection:**
```powershell
python test_ollama_connection.py
```

## Troubleshooting

**"Authentication failed"**
- Check your API key is correct
- Make sure there are no extra spaces
- Try using your device key instead

**"Cannot connect"**
- Check your OLLAMA_URL is correct
- Verify internet connection
- Check Ollama cloud service status

**"No models found"**
- Your model might need to be pulled first
- Check if the model name matches what's available

## Need Help?

1. **Check your Ollama dashboard** - URL and keys are there
2. **Test connection first** - Run `python test_ollama_connection.py`
3. **Start with text mode** - Run `python seamless_trading_assistant.py` (easier to debug)

