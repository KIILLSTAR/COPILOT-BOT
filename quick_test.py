#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Quick Test - Test Jupiter Data and Voice (without Ollama)
"""
import sys

# Set UTF-8 encoding for Windows
if sys.platform == 'win32':
    try:
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    except:
        pass

print("Quick Test - Jupiter Data & Voice")
print("=" * 60)

# Test 1: Jupiter API
print("\n1. Testing Jupiter API...")
try:
    from core.jupiter_api import JupiterAPI, ETHPerpTrader
    jupiter_api = JupiterAPI()
    eth_trader = ETHPerpTrader(jupiter_api)
    
    price = eth_trader.get_eth_price()
    if price:
        print(f"   OK - Jupiter ETH Price: ${price:,.2f}")
    else:
        print("   WARNING - Could not get Jupiter price (check internet)")
except Exception as e:
    print(f"   ERROR: {e}")

# Test 2: Voice TTS
print("\n2. Testing Voice Output...")
try:
    import pyttsx3
    engine = pyttsx3.init()
    print("   OK - Voice engine initialized")
    
    # Test speak
    test_text = "Voice test successful"
    print(f"   Speaking: {test_text}")
    engine.say(test_text)
    engine.runAndWait()
    print("   OK - Voice output works!")
except Exception as e:
    print(f"   ERROR: {e}")

# Test 3: Voice Recognition
print("\n3. Testing Voice Recognition...")
print("   (This requires microphone access)")
try:
    import speech_recognition as sr
    r = sr.Recognizer()
    print("   OK - Speech recognition initialized")
    print("   Note: Voice input test skipped (requires microphone)")
except Exception as e:
    print(f"   ERROR: {e}")

# Test 4: Configuration
print("\n4. Testing Configuration...")
try:
    from ai_assistant_config import get_config
    config = get_config()
    print(f"   OK - Config loaded")
    print(f"   Standalone mode: {config.get('standalone_mode')}")
    print(f"   Jupiter Perps: {config.get('use_jupiter_perps')}")
except Exception as e:
    print(f"   ERROR: {e}")

print("\n" + "=" * 60)
print("Test Complete!")
print("=" * 60)
print("\nNext: Set Ollama URL for AI recommendations:")
print("  $env:OLLAMA_URL='your-ollama-cloud-url'")
print("\nThen run:")
print("  python voice_assistant.py")
print("\nOr test text-only:")
print("  python seamless_trading_assistant.py")

