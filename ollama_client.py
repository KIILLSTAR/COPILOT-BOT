#!/usr/bin/env python3
"""
Ollama Client for Live Trading AI Assistant
Connects to Ollama cloud models for trading analysis and recommendations
"""
import requests
import json
import os
from typing import Dict, Any, Optional, List
from datetime import datetime

# Load .env file if available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # python-dotenv not installed, environment variables must be set manually


class OllamaClient:
    """
    Client for interacting with Ollama cloud models
    Supports both local Ollama instances and cloud-hosted models
    """
    
    def __init__(self, base_url: Optional[str] = None, model_name: str = "llama3.2", api_key: Optional[str] = None):
        """
        Initialize Ollama client
        
        Args:
            base_url: URL of Ollama server (default: auto-detect from env or use cloud)
                     For cloud: use your cloud instance URL or set OLLAMA_URL env var
                     Examples: "https://api.ollama.ai/v1" or "https://your-cloud-instance.com"
            model_name: Name of the model to use (e.g., "llama3.2", "mistral", "qwen")
            api_key: API key for authentication (default: from OLLAMA_API_KEY env var)
        """
        import os
        
        # Auto-detect: prefer env var, then cloud default, then localhost fallback
        if base_url is None:
            base_url = os.getenv('OLLAMA_URL') or os.getenv('OLLAMA_CLOUD_URL')
            if base_url is None:
                # Default to cloud service if available, otherwise localhost
                base_url = "https://api.ollama.ai/v1"  # Cloud default
                # Fallback to localhost for backwards compatibility
                # base_url = "http://localhost:11434"
        
        # Get API key from parameter or environment
        if api_key is None:
            api_key = os.getenv('OLLAMA_API_KEY') or os.getenv('OLLAMA_DEVICE_KEY')
        
        self.base_url = base_url.rstrip('/')
        self.model_name = model_name
        self.api_key = api_key
        
        # Handle different API endpoint patterns
        if '/api' in self.base_url or '/v1' in self.base_url:
            # Cloud service format
            self.api_url = self.base_url if self.base_url.endswith('/api') or self.base_url.endswith('/v1') else f"{self.base_url}/api"
        else:
            # Local format
            self.api_url = f"{self.base_url}/api"
            
        self.chat_url = f"{self.api_url}/chat"
        self.generate_url = f"{self.api_url}/generate"
        
        # Set up headers for authenticated requests
        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        
        # Add API key to headers if provided
        if self.api_key:
            self.headers['Authorization'] = f'Bearer {self.api_key}'
            # Also try Ollama-specific header format
            self.headers['Ollama-Api-Key'] = self.api_key
        
    def test_connection(self) -> bool:
        """
        Test if Ollama server is accessible
        
        Returns:
            True if connection successful, False otherwise
        """
        try:
            response = requests.get(
                f"{self.base_url}/api/tags", 
                headers=self.headers,
                timeout=5
            )
            if response.status_code == 200:
                return True
            elif response.status_code == 401:
                print("❌ Authentication failed - check your API key")
                return False
            else:
                print(f"⚠️ Connection test failed: Status {response.status_code}")
                return False
        except Exception as e:
            print(f"⚠️ Connection test failed: {e}")
            return False
    
    def list_models(self) -> List[str]:
        """
        List available models on the Ollama server
        
        Returns:
            List of available model names
        """
        try:
            response = requests.get(
                f"{self.base_url}/api/tags", 
                headers=self.headers,
                timeout=10
            )
            if response.status_code == 200:
                data = response.json()
                models = [model['name'] for model in data.get('models', [])]
                return models
            elif response.status_code == 401:
                print("❌ Authentication failed - check your API key")
                return []
            return []
        except Exception as e:
            print(f"⚠️ Error listing models: {e}")
            return []
    
    def chat(self, messages: List[Dict[str, str]], stream: bool = False) -> str:
        """
        Send chat messages to Ollama model
        
        Args:
            messages: List of message dicts with 'role' and 'content'
                     Example: [{"role": "user", "content": "Hello"}]
            stream: Whether to stream the response (default: False)
        
        Returns:
            Model's response text
        """
        payload = {
            "model": self.model_name,
            "messages": messages,
            "stream": stream
        }
        
        try:
            response = requests.post(
                self.chat_url,
                json=payload,
                headers=self.headers,
                timeout=60,
                stream=stream
            )
            
            if stream:
                # Handle streaming response
                full_response = ""
                for line in response.iter_lines():
                    if line:
                        try:
                            data = json.loads(line)
                            if 'message' in data and 'content' in data['message']:
                                content = data['message']['content']
                                full_response += content
                                if data.get('done', False):
                                    break
                        except json.JSONDecodeError:
                            continue
                return full_response
            else:
                # Handle non-streaming response
                response.raise_for_status()
                data = response.json()
                return data.get('message', {}).get('content', '')
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Error communicating with Ollama: {e}")
            return f"Error: {str(e)}"
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            return f"Error: {str(e)}"
    
    def generate(self, prompt: str, stream: bool = False, **kwargs) -> str:
        """
        Generate text from a prompt (simple generation, no chat history)
        
        Args:
            prompt: The prompt text
            stream: Whether to stream the response
            **kwargs: Additional parameters (temperature, top_p, etc.)
        
        Returns:
            Generated text
        """
        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": stream,
            **kwargs
        }
        
        try:
            response = requests.post(
                self.generate_url,
                json=payload,
                headers=self.headers,
                timeout=60,
                stream=stream
            )
            
            if stream:
                full_response = ""
                for line in response.iter_lines():
                    if line:
                        try:
                            data = json.loads(line)
                            if 'response' in data:
                                full_response += data['response']
                            if data.get('done', False):
                                break
                        except json.JSONDecodeError:
                            continue
                return full_response
            else:
                response.raise_for_status()
                data = response.json()
                return data.get('response', '')
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Error generating text: {e}")
            return f"Error: {str(e)}"
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            return f"Error: {str(e)}"
    
    def analyze_trading_data(self, market_data: Dict[str, Any], context: str = "") -> Dict[str, Any]:
        """
        Analyze trading data and get AI recommendations
        
        Args:
            market_data: Dictionary containing market indicators, prices, etc.
            context: Additional context or instructions
        
        Returns:
            Dictionary with analysis and recommendations
        """
        # Format market data for AI
        data_summary = self._format_market_data(market_data)
        
        system_prompt = """You are an expert cryptocurrency trading assistant. 
Analyze the provided market data and provide clear, actionable trading recommendations.
Focus on:
1. Key market indicators and what they mean
2. Risk assessment
3. Specific trading action recommendation (LONG, SHORT, or HOLD)
4. Confidence level and reasoning
5. Important warnings or cautions

Be concise but thorough. Format your response as structured analysis."""
        
        user_prompt = f"""Market Data:
{data_summary}

{context if context else ''}

Please provide a comprehensive trading analysis and recommendation."""
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        analysis = self.chat(messages)
        
        return {
            "timestamp": datetime.now().isoformat(),
            "model": self.model_name,
            "analysis": analysis,
            "market_data_snapshot": market_data
        }
    
    def _format_market_data(self, market_data: Dict[str, Any]) -> str:
        """Format market data into readable string for AI"""
        lines = []
        for key, value in market_data.items():
            if isinstance(value, (int, float)):
                lines.append(f"{key}: {value}")
            elif isinstance(value, dict):
                lines.append(f"{key}: {json.dumps(value, indent=2)}")
            else:
                lines.append(f"{key}: {str(value)}")
        return "\n".join(lines)


def test_ollama_setup():
    """Test function to verify Ollama setup"""
    print("🔍 Testing Ollama Setup...")
    print("=" * 50)
    
    # Try default local connection
    client = OllamaClient()
    
    print(f"📍 Base URL: {client.base_url}")
    print(f"🤖 Model: {client.model_name}")
    
    # Test connection
    print("\n1️⃣ Testing connection...")
    if client.test_connection():
        print("✅ Connection successful!")
    else:
        print("❌ Connection failed!")
        print("💡 Make sure Ollama is running:")
        print("   - For local: Run 'ollama serve' or install Ollama")
        print("   - For cloud: Update base_url to your cloud instance URL")
        return False
    
    # List models
    print("\n2️⃣ Listing available models...")
    models = client.list_models()
    if models:
        print(f"✅ Found {len(models)} model(s):")
        for model in models:
            print(f"   - {model}")
    else:
        print("⚠️ No models found")
        print("💡 Pull a model first: 'ollama pull llama3.2'")
    
    # Test chat
    print("\n3️⃣ Testing chat...")
    try:
        response = client.chat([{"role": "user", "content": "Say 'Hello' if you can hear me."}])
        print(f"✅ Response: {response[:100]}...")
        return True
    except Exception as e:
        print(f"❌ Chat test failed: {e}")
        return False


if __name__ == "__main__":
    test_ollama_setup()

