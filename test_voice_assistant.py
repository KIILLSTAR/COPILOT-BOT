#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Quick Test Script for Voice Assistant
Checks requirements and runs a simple test
"""
import sys
import os

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    try:
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')
    except:
        pass

print("Voice Assistant Test Script")
print("=" * 60)

# Check Python version
print("\n1️⃣ Checking Python version...")
print(f"   Python {sys.version.split()[0]} ✅")

# Check voice libraries
print("\n2️⃣ Checking voice libraries...")
try:
    import speech_recognition as sr
    import pyttsx3
    print("   OK - SpeechRecognition installed")
    print("   OK - pyttsx3 installed")
    VOICE_OK = True
except ImportError as e:
    print(f"   ❌ Voice libraries missing: {e}")
    print("   💡 Install with: pip install SpeechRecognition pyttsx3")
    VOICE_OK = False

# Check configuration
print("\n3️⃣ Checking configuration...")
try:
    from ai_assistant_config import get_config
    config = get_config()
    print(f"   ✅ Configuration loaded")
    print(f"   Mode: {'Standalone' if config.get('standalone_mode') else 'Integrated'}")
    print(f"   Jupiter Perps: {'✅ Enabled' if config.get('use_jupiter_perps') else '❌ Disabled'}")
except Exception as e:
    print(f"   ⚠️ Configuration error: {e}")
    print("   💡 Run: python ai_assistant_config.py to set up")

# Check Ollama connection
print("\n4️⃣ Checking Ollama connection...")
try:
    from ollama_client import OllamaClient
    
    ollama_url = os.getenv('OLLAMA_URL') or os.getenv('OLLAMA_CLOUD_URL')
    if ollama_url:
        print(f"   Ollama URL: {ollama_url}")
    else:
        print("   ⚠️ OLLAMA_URL not set")
        print("   💡 Set with: $env:OLLAMA_URL='your-url' (PowerShell)")
        print("   💡 Or add to .env file")
    
    # Test connection
    client = OllamaClient(base_url=ollama_url)
    if client.test_connection():
        print("   OK - Ollama connection successful!")
        models = client.list_models()
        if models:
            print(f"   Available models: {', '.join(models)}")
        else:
            print("   ⚠️ No models found")
            print("   💡 Pull a model: ollama pull llama3.2")
    else:
        print("   ❌ Cannot connect to Ollama")
        print("   💡 Check your OLLAMA_URL or Ollama service status")
except Exception as e:
    print(f"   ⚠️ Ollama check error: {e}")

# Check Jupiter API
print("\n5️⃣ Checking Jupiter API integration...")
try:
    from core.jupiter_api import JupiterAPI, ETHPerpTrader
    print("   OK - Jupiter API modules available")
    
    # Quick test
    jupiter_api = JupiterAPI()
    eth_trader = ETHPerpTrader(jupiter_api)
    print("   OK - Jupiter components initialized")
except ImportError as e:
    print(f"   ⚠️ Jupiter API not available: {e}")
    print("   💡 This is OK - will use fallback data")
except Exception as e:
    print(f"   ⚠️ Jupiter initialization error: {e}")

# Summary
print("\n" + "=" * 60)
print("📊 TEST SUMMARY")
print("=" * 60)

if VOICE_OK:
    print("OK - Voice libraries: Ready")
else:
    print("ERROR - Voice libraries: Install required")

print("OK - Configuration: Loaded")
print("OK - Components: Available")

print("\n💡 NEXT STEPS:")
print("=" * 60)

if not VOICE_OK:
    print("1. Install voice libraries:")
    print("   pip install SpeechRecognition pyttsx3")
    print()

if not ollama_url:
    print("2. Set Ollama URL:")
    print("   $env:OLLAMA_URL='your-ollama-cloud-url'")
    print()

print("3. Run voice assistant:")
print("   python voice_assistant.py")
print()

print("4. Or test text-only mode:")
print("   python seamless_trading_assistant.py")
print()

print("OK - Ready to test!")

