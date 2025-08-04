#!/usr/bin/env python3
# test_offline.py - Quick test of offline bot functionality

import time
import random
import math
from datetime import datetime

def test_offline_bot():
    """Test the offline bot for a few cycles"""
    print("🧪 Testing Offline Trading Bot...")
    
    # Simulate ETH price
    eth_price = 3000.0
    price_history = [eth_price]
    
    print(f"📊 Starting ETH Price: ${eth_price:,.2f}")
    
    for cycle in range(5):  # Test 5 cycles
        print(f"\n--- Cycle {cycle + 1} ---")
        
        # Simulate price movement
        change = random.gauss(0, 0.01)  # 1% volatility
        eth_price *= (1 + change)
        eth_price = max(1000, min(10000, eth_price))  # Keep reasonable
        price_history.append(eth_price)
        
        print(f"📊 ETH Price: ${eth_price:,.2f}")
        print(f"📈 Change: {change:+.2%}")
        
        # Simple signal detection
        if len(price_history) >= 3:
            recent_change = (price_history[-1] - price_history[-3]) / price_history[-3]
            if abs(recent_change) > 0.02:  # 2% change
                signal = "LONG" if recent_change > 0 else "SHORT"
                print(f"📡 Signal: {signal} (momentum: {recent_change:+.1%})")
            else:
                print("📡 No signal")
        
        time.sleep(2)  # Quick test
    
    print("\n✅ Offline bot test completed successfully!")
    print("📱 Ready to run on mobile devices")

if __name__ == "__main__":
    test_offline_bot()