#!/usr/bin/env python3
"""
Simple test script to verify Ollama setup for trading AI assistant
"""
import sys

def main():
    print("🧪 Testing Ollama Setup for Trading AI Assistant")
    print("=" * 60)
    
    try:
        # Test 1: Import modules
        print("\n1️⃣ Testing imports...")
        from ollama_client import OllamaClient
        from trading_ai_assistant import TradingAIAssistant
        print("✅ Imports successful!")
        
        # Test 2: Test Ollama connection
        print("\n2️⃣ Testing Ollama connection...")
        client = OllamaClient()
        if client.test_connection():
            print("✅ Ollama connection successful!")
        else:
            print("❌ Cannot connect to Ollama!")
            print("\n💡 Solutions:")
            print("   - Make sure Ollama is running: 'ollama serve'")
            print("   - Install Ollama from: https://ollama.com")
            print("   - For cloud: Update base_url in the code")
            return False
        
        # Test 3: List models
        print("\n3️⃣ Checking available models...")
        models = client.list_models()
        if models:
            print(f"✅ Found {len(models)} model(s):")
            for model in models:
                print(f"   - {model}")
        else:
            print("⚠️ No models found!")
            print("\n💡 Pull a model:")
            print("   - ollama pull llama3.2")
            print("   - ollama pull mistral")
            print("   - ollama pull qwen2.5")
            return False
        
        # Test 4: Simple chat test
        print("\n4️⃣ Testing AI chat...")
        try:
            response = client.chat([{
                "role": "user", 
                "content": "Respond with just 'OK' if you can hear me."
            }])
            print(f"✅ Chat test successful!")
            print(f"   Response: {response[:100]}...")
        except Exception as e:
            print(f"❌ Chat test failed: {e}")
            return False
        
        # Test 5: Trading assistant initialization
        print("\n5️⃣ Testing Trading AI Assistant...")
        try:
            assistant = TradingAIAssistant(
                ollama_url="http://localhost:11434",
                model_name=client.model_name
            )
            print("✅ Trading AI Assistant initialized!")
        except Exception as e:
            print(f"❌ Assistant initialization failed: {e}")
            return False
        
        # Test 6: Quick recommendation test
        print("\n6️⃣ Testing quick recommendation...")
        try:
            quick_rec = assistant.get_quick_recommendation(
                price=3500.0,
                indicators={"rsi": 45.0, "ema_trend": "bullish"}
            )
            print(f"✅ Quick recommendation test successful!")
            print(f"   Response: {quick_rec[:150]}...")
        except Exception as e:
            print(f"❌ Quick recommendation test failed: {e}")
            return False
        
        # All tests passed
        print("\n" + "=" * 60)
        print("✅ ALL TESTS PASSED!")
        print("=" * 60)
        print("\n🎉 Your Ollama setup is ready for trading AI assistant!")
        print("\n📝 Next steps:")
        print("   1. Run the demo: python trading_ai_assistant.py")
        print("   2. Integrate with your trading bot")
        print("   3. (Optional) Set up Comet ML for tracking")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("\n💡 Make sure you have all dependencies:")
        print("   pip install requests")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

