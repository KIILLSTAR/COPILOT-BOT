#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Ollama Connection with API Key
Helps you test your Ollama cloud connection
"""
import os
import sys

# Set UTF-8 encoding for Windows
if sys.platform == 'win32':
    try:
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    except:
        pass

print("Ollama Connection Test")
print("=" * 60)

# Check for API key
api_key = os.getenv('OLLAMA_API_KEY') or os.getenv('OLLAMA_DEVICE_KEY')
ollama_url = os.getenv('OLLAMA_URL') or os.getenv('OLLAMA_CLOUD_URL')

print("\n1. Checking Configuration...")
if ollama_url:
    print(f"   OLLAMA_URL: {ollama_url}")
else:
    print("   WARNING: OLLAMA_URL not set")
    print("   Set with: $env:OLLAMA_URL='your-url'")
    ollama_url = input("\n   Enter your Ollama URL (or press Enter for default): ").strip()
    if not ollama_url:
        ollama_url = "https://api.ollama.ai/v1"

if api_key:
    print(f"   API Key: {'*' * (len(api_key) - 4) + api_key[-4:] if len(api_key) > 4 else '***'}")
else:
    print("   WARNING: OLLAMA_API_KEY not set")
    print("   Set with: $env:OLLAMA_API_KEY='your-key'")
    api_key = input("\n   Enter your API/Device Key (or press Enter to skip): ").strip()

print("\n2. Testing Connection...")
try:
    from ollama_client import OllamaClient
    
    client = OllamaClient(
        base_url=ollama_url,
        api_key=api_key,
        model_name="llama3.2"
    )
    
    if client.test_connection():
        print("   OK - Connection successful!")
        
        print("\n3. Listing Models...")
        models = client.list_models()
        if models:
            print(f"   Found {len(models)} model(s):")
            for model in models:
                print(f"     - {model}")
        else:
            print("   WARNING - No models found")
            print("   Your model might need to be pulled first")
        
        print("\n4. Testing Chat...")
        try:
            response = client.chat([{
                "role": "user",
                "content": "Say 'Hello' if you can hear me."
            }])
            print(f"   Response: {response[:100]}...")
            print("   OK - Chat test successful!")
        except Exception as e:
            print(f"   ERROR: {e}")
        
        print("\n" + "=" * 60)
        print("SUCCESS - Ollama connection working!")
        print("=" * 60)
        print("\nYou can now run:")
        print("  python voice_assistant.py")
        print("  python seamless_trading_assistant.py")
        
    else:
        print("   ERROR - Connection failed")
        print("\nTroubleshooting:")
        print("  1. Check your OLLAMA_URL is correct")
        print("  2. Verify your API key is correct")
        print("  3. Make sure you have internet connection")
        print("  4. Check Ollama cloud service status")
        
except ImportError as e:
    print(f"   ERROR: {e}")
    print("   Make sure ollama_client.py is in the project directory")
except Exception as e:
    print(f"   ERROR: {e}")
    import traceback
    traceback.print_exc()

