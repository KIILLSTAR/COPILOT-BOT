#!/usr/bin/env python3
"""
Live Trading AI Assistant
Uses Ollama to analyze trading screens and live data for faster, more accurate recommendations
"""
import json
from typing import Dict, Any, Optional, List
from datetime import datetime
from ollama_client import OllamaClient


class TradingAIAssistant:
    """
    AI-powered trading assistant that analyzes market data and provides recommendations
    Uses Ollama cloud models for fast analysis and decision-making
    """
    
    def __init__(self, 
                 ollama_url: str = "http://localhost:11434",
                 model_name: str = "llama3.2",
                 enable_comet: bool = False):
        """
        Initialize the trading AI assistant
        
        Args:
            ollama_url: URL of Ollama server (local or cloud)
            model_name: Name of the model to use
            enable_comet: Whether to enable Comet ML tracking (requires setup)
        """
        self.ollama = OllamaClient(base_url=ollama_url, model_name=model_name)
        self.enable_comet = enable_comet
        self.conversation_history = []
        
        # Initialize Comet if enabled
        if enable_comet:
            try:
                import comet_ml
                self.comet = comet_ml.Experiment()
                print("✅ Comet ML initialized")
            except ImportError:
                print("⚠️ Comet ML not installed. Install with: pip install comet-ml")
                self.enable_comet = False
                self.comet = None
        else:
            self.comet = None
    
    def analyze_screen_data(self, screen_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze data from your trading screen
        
        This can include:
        - Current prices
        - Charts/indicators
        - Order book data
        - Recent trades
        - Portfolio status
        
        Args:
            screen_data: Dictionary containing all visible screen data
        
        Returns:
            Analysis and recommendations
        """
        # Format screen data for analysis
        analysis_prompt = self._build_screen_analysis_prompt(screen_data)
        
        messages = [
            {
                "role": "system",
                "content": """You are a professional cryptocurrency trading assistant.
Analyze the trading screen data provided and give immediate, actionable insights.
Focus on:
- Current market conditions
- Key price levels to watch
- Trading opportunities
- Risk warnings
- Specific action recommendations"""
            },
            {
                "role": "user",
                "content": analysis_prompt
            }
        ]
        
        # Get AI analysis
        analysis_text = self.ollama.chat(messages)
        
        # Parse structured response if possible
        recommendation = self._extract_recommendation(analysis_text)
        
        result = {
            "timestamp": datetime.now().isoformat(),
            "recommendation": recommendation,
            "full_analysis": analysis_text,
            "screen_data": screen_data
        }
        
        # Log to Comet if enabled
        if self.enable_comet and self.comet:
            self.comet.log_metric("screen_analysis_count", 1)
            self.comet.log_other("recommendation", recommendation.get("action", "UNKNOWN"))
        
        return result
    
    def analyze_live_data(self, 
                         market_data: Dict[str, Any],
                         portfolio: Dict[str, Any],
                         trade_history: List[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Analyze live market data and provide trading recommendations
        
        Args:
            market_data: Real-time market data (prices, indicators, etc.)
            portfolio: Current portfolio status
            trade_history: Recent trade history for context
        
        Returns:
            Comprehensive analysis and recommendation
        """
        # Build comprehensive prompt
        context = self._build_live_data_context(market_data, portfolio, trade_history)
        
        messages = [
            {
                "role": "system",
                "content": """You are an advanced cryptocurrency trading AI assistant.
Analyze live market data, portfolio status, and recent trade history.
Provide:
1. Market Assessment (bullish/bearish/neutral)
2. Key Indicators Analysis
3. Portfolio Risk Assessment
4. Action Recommendation (LONG/SHORT/HOLD)
5. Confidence Score (1-10)
6. Reasoning
7. Entry/Exit Suggestions
8. Risk Management Notes"""
            },
            {
                "role": "user",
                "content": context
            }
        ]
        
        # Add conversation history for context
        if self.conversation_history:
            messages = self.conversation_history[-3:] + messages  # Last 3 exchanges
        
        # Get AI analysis
        analysis = self.ollama.chat(messages)
        
        # Store in conversation history
        self.conversation_history.append({"role": "user", "content": context})
        self.conversation_history.append({"role": "assistant", "content": analysis})
        
        # Keep history manageable (last 20 messages)
        if len(self.conversation_history) > 20:
            self.conversation_history = self.conversation_history[-20:]
        
        # Extract structured recommendation
        recommendation = self._extract_recommendation(analysis)
        
        result = {
            "timestamp": datetime.now().isoformat(),
            "recommendation": recommendation,
            "analysis": analysis,
            "market_data": market_data,
            "portfolio": portfolio
        }
        
        # Log to Comet if enabled
        if self.enable_comet and self.comet:
            self._log_to_comet(result)
        
        return result
    
    def get_quick_recommendation(self, price: float, indicators: Dict[str, float]) -> str:
        """
        Get a quick trading recommendation for rapid decision-making
        
        Args:
            price: Current price
            indicators: Key indicators (RSI, EMA, etc.)
        
        Returns:
            Quick recommendation text
        """
        prompt = f"""Quick trading recommendation needed:
Price: {price}
RSI: {indicators.get('rsi', 'N/A')}
EMA Trend: {indicators.get('ema_trend', 'N/A')}
Volume: {indicators.get('volume', 'N/A')}

Give ONE WORD recommendation: LONG, SHORT, or HOLD. Then one sentence explanation."""
        
        response = self.ollama.generate(prompt, temperature=0.3)  # Lower temperature for more consistent results
        return response.strip()
    
    def _build_screen_analysis_prompt(self, screen_data: Dict[str, Any]) -> str:
        """Build prompt from screen data"""
        lines = ["TRADING SCREEN DATA:", "=" * 40]
        
        if 'price' in screen_data:
            lines.append(f"Current Price: {screen_data['price']}")
        if 'indicators' in screen_data:
            lines.append(f"Indicators: {json.dumps(screen_data['indicators'], indent=2)}")
        if 'order_book' in screen_data:
            lines.append(f"Order Book: {json.dumps(screen_data['order_book'], indent=2)}")
        if 'positions' in screen_data:
            lines.append(f"Open Positions: {json.dumps(screen_data['positions'], indent=2)}")
        if 'balance' in screen_data:
            lines.append(f"Balance: {screen_data['balance']}")
        
        lines.append("\nAnalyze this screen and provide trading recommendations:")
        return "\n".join(lines)
    
    def _build_live_data_context(self, 
                                 market_data: Dict[str, Any],
                                 portfolio: Dict[str, Any],
                                 trade_history: Optional[List[Dict[str, Any]]] = None) -> str:
        """Build context string from live data"""
        lines = ["LIVE MARKET ANALYSIS REQUEST", "=" * 50]
        
        lines.append("\nMARKET DATA:")
        for key, value in market_data.items():
            if isinstance(value, (int, float)):
                lines.append(f"  {key}: {value}")
            elif isinstance(value, dict):
                lines.append(f"  {key}:")
                for k, v in value.items():
                    lines.append(f"    {k}: {v}")
        
        lines.append("\nPORTFOLIO STATUS:")
        for key, value in portfolio.items():
            lines.append(f"  {key}: {value}")
        
        if trade_history:
            lines.append("\nRECENT TRADES (last 3):")
            for i, trade in enumerate(trade_history[-3:], 1):
                lines.append(f"  Trade {i}: {json.dumps(trade, indent=4)}")
        
        lines.append("\nPlease provide comprehensive analysis and recommendation:")
        return "\n".join(lines)
    
    def _extract_recommendation(self, analysis_text: str) -> Dict[str, Any]:
        """Extract structured recommendation from analysis text"""
        recommendation = {
            "action": "HOLD",  # Default
            "confidence": 5,  # Default medium confidence
            "reasoning": analysis_text,
            "entry_price": None,
            "stop_loss": None,
            "take_profit": None
        }
        
        # Try to extract action (LONG/SHORT/HOLD)
        analysis_upper = analysis_text.upper()
        if "LONG" in analysis_upper or "BUY" in analysis_upper:
            recommendation["action"] = "LONG"
        elif "SHORT" in analysis_upper or "SELL" in analysis_upper:
            recommendation["action"] = "SHORT"
        
        # Try to extract confidence score
        import re
        confidence_match = re.search(r'confidence[:\s]+(\d+)', analysis_upper)
        if confidence_match:
            recommendation["confidence"] = int(confidence_match.group(1))
        
        # Try to extract price levels
        price_match = re.search(r'(?:entry|price)[:\s]+\$?(\d+\.?\d*)', analysis_upper)
        if price_match:
            recommendation["entry_price"] = float(price_match.group(1))
        
        return recommendation
    
    def _log_to_comet(self, result: Dict[str, Any]):
        """Log analysis results to Comet ML"""
        if not self.comet:
            return
        
        try:
            # Log metrics
            self.comet.log_metric("analysis_timestamp", datetime.now().timestamp())
            
            # Log recommendation
            rec = result.get("recommendation", {})
            action_map = {"LONG": 1, "SHORT": -1, "HOLD": 0}
            self.comet.log_metric("recommendation_value", 
                                 action_map.get(rec.get("action", "HOLD"), 0))
            self.comet.log_metric("confidence", rec.get("confidence", 5))
            
            # Log market data
            market_data = result.get("market_data", {})
            if "price" in market_data:
                self.comet.log_metric("price", market_data["price"])
            if "rsi" in market_data:
                self.comet.log_metric("rsi", market_data["rsi"])
            
            # Log text analysis
            self.comet.log_text(result.get("analysis", ""))
            
        except Exception as e:
            print(f"⚠️ Error logging to Comet: {e}")


def demo_trading_assistant():
    """Demo the trading AI assistant"""
    print("🚀 Trading AI Assistant Demo")
    print("=" * 50)
    
    # Initialize assistant
    print("\n1️⃣ Initializing AI Assistant...")
    assistant = TradingAIAssistant(
        ollama_url="http://localhost:11434",
        model_name="llama3.2"
    )
    
    # Test connection
    print("\n2️⃣ Testing Ollama connection...")
    if not assistant.ollama.test_connection():
        print("❌ Cannot connect to Ollama!")
        print("💡 Make sure Ollama is running: 'ollama serve'")
        return
    
    print("✅ Connected to Ollama!")
    
    # Demo: Analyze mock screen data
    print("\n3️⃣ Analyzing mock screen data...")
    screen_data = {
        "price": 3500.0,
        "indicators": {
            "rsi": 45.0,
            "ema_12": 3480.0,
            "ema_26": 3520.0,
            "volume_24h": 1500000.0
        },
        "balance": 10000.0,
        "positions": []
    }
    
    result = assistant.analyze_screen_data(screen_data)
    print(f"\n📊 Recommendation: {result['recommendation']['action']}")
    print(f"📈 Confidence: {result['recommendation']['confidence']}/10")
    print(f"\n💬 Analysis:\n{result['full_analysis'][:300]}...")
    
    # Demo: Quick recommendation
    print("\n4️⃣ Getting quick recommendation...")
    quick_rec = assistant.get_quick_recommendation(
        price=3500.0,
        indicators={"rsi": 45.0, "ema_trend": "bullish", "volume": "high"}
    )
    print(f"⚡ Quick Rec: {quick_rec[:200]}...")
    
    print("\n✅ Demo complete!")


if __name__ == "__main__":
    demo_trading_assistant()

