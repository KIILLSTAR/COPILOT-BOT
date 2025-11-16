#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Quick Setup and Run Script
Helps you set up Ollama credentials and run the voice assistant
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

print("Voice Trading Assistant - Setup & Run")
print("=" * 60)

# Check current settings
ollama_url = os.getenv('OLLAMA_URL')
api_key = os.getenv('OLLAMA_API_KEY') or os.getenv('OLLAMA_DEVICE_KEY')

print("\nCurrent Settings:")
if ollama_url:
    print(f"  OLLAMA_URL: {ollama_url}")
else:
    print("  OLLAMA_URL: NOT SET")

if api_key:
    masked_key = '*' * (len(api_key) - 4) + api_key[-4:] if len(api_key) > 4 else '***'
    print(f"  API Key: {masked_key}")
else:
    print("  API Key: NOT SET")

print("\n" + "=" * 60)
print("To set your credentials, run in PowerShell:")
print("=" * 60)
print("\n  $env:OLLAMA_URL='your-ollama-cloud-url'")
print("  $env:OLLAMA_API_KEY='your-api-key'")
print("\nOr edit the .env file in your project root:")
print("  C:\\Users\\natha\\OneDrive\\Desktop\\COPILOT REPO\\COPILOT-BOT\\.env")
print("\n" + "=" * 60)

# Try to run the voice assistant
if not ollama_url or not api_key:
    print("\nWARNING: Ollama credentials not set!")
    print("\nPlease set them first, then run:")
    print("  python voice_assistant.py")
    print("\nOr set them now in this PowerShell window, then re-run this script")
    sys.exit(1)

print("\nTesting connection...")
try:
    from ollama_client import OllamaClient
    
    client = OllamaClient(
        base_url=ollama_url,
        api_key=api_key,
        model_name="llama3.2"
    )
    
    if client.test_connection():
        print("OK - Connection successful!")
        print("\nStarting voice assistant...")
        print("=" * 60)
        
        # Import and run voice assistant
        from voice_assistant import main
        main()
    else:
        print("ERROR - Connection failed")
        print("Please check your URL and API key")
        
except ImportError as e:
    print(f"ERROR: {e}")
    print("Make sure all files are in the project directory")
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()

