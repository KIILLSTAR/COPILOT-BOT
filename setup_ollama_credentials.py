#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple script to help you set up Ollama credentials
"""
import os

print("Ollama Credentials Setup")
print("=" * 60)

print("\nYou need:")
print("1. Your Ollama Cloud URL")
print("2. Your API Key or Device Key")

print("\n" + "=" * 60)
print("Option 1: Set in PowerShell (for this session)")
print("=" * 60)
print("\nRun these commands:")
print('  $env:OLLAMA_URL="your-ollama-cloud-url-here"')
print('  $env:OLLAMA_API_KEY="your-api-key-here"')

print("\n" + "=" * 60)
print("Option 2: Edit .env file (permanent)")
print("=" * 60)
env_path = os.path.join(os.getcwd(), '.env')
print(f"\n1. Open this file in Notepad:")
print(f"   {env_path}")
print("\n2. Add these lines:")
print("   OLLAMA_URL=your-ollama-cloud-url-here")
print("   OLLAMA_API_KEY=your-api-key-here")
print("   OLLAMA_MODEL=llama3.2")

print("\n" + "=" * 60)
print("Common Ollama Cloud URLs:")
print("=" * 60)
print("  - Default Ollama Cloud: https://api.ollama.ai/v1")
print("  - Custom instance: Check your Ollama dashboard")
print("  - Local Ollama: http://localhost:11434")

print("\n" + "=" * 60)
print("Your API Key:")
print("=" * 60)
print("  - Use your API key from Ollama's website")
print("  - Or use your Device Key (works the same)")
print("  - Set as OLLAMA_API_KEY or OLLAMA_DEVICE_KEY")

print("\n" + "=" * 60)
print("After setting credentials:")
print("=" * 60)
print("  python voice_assistant.py")
print("\nOr test connection:")
print("  python test_ollama_connection.py")

print("\nPress Enter to continue...")
input()

