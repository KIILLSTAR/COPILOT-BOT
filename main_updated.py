#!/usr/bin/env python3
"""
Unified Trading Bot - Updated Version
Automatically detects platform and adapts for optimal performance
Beginner-friendly with clear explanations and enhanced features
"""
import os
import sys
import time
import platform
import threading
import json
from datetime import datetime
from typing import Dict, Any, Optional

class PlatformDetector:
    """Detects the current platform and capabilities"""
    
    @staticmethod
    def detect_platform() -> Dict[str, Any]:
        """Detect current platform and capabilities"""
        info = {
            'os': platform.system().lower(),
            'is_mobile': False,
            'has_internet': True,
            'has_display': True,
            'is_limited': False,
            'recommended_mode': 'standard',
            'version': '2.0.0'
        }
        
        # Detect mobile platforms
        if info['os'] in ['android', 'ios']:
            info['is_mobile'] = True
            info['recommended_mode'] = 'mobile'
        elif 'replit' in os.environ.get('REPL_ID', '').lower():
            info['is_mobile'] = True
            info['recommended_mode'] = 'mobile'
        elif 'colab' in os.environ.get('COLAB_GPU', '').lower():
            info['is_mobile'] = True
            info['recommended_mode'] = 'mobile'
        
        # Check for limited environments
        if info['is_mobile'] or os.path.exists('/proc/version'):
            info['is_limited'] = True
        
        # Test internet connectivity
        try:
            import requests
            requests.get('https://api.coingecko.com/api/v3/ping', timeout=5)
        except:
            info['has_internet'] = False
            info['recommended_mode'] = 'offline'
        
        # Check for display capabilities
        if 'DISPLAY' not in os.environ and info['os'] == 'linux':
            info['has_display'] = False
        
        return info

class UnifiedTradingBot:
    """
    Unified trading bot that adapts to any platform
    Enhanced with better error handling and performance tracking
    """
    
    def __init__(self, platform_info: Dict[str, Any]):
        self.platform_info = platform_info
        self.running = False
        self.cycle_count = 0
        self.balance = 10000.0
        self.positions = []
        self.trade_history = []
        self.price_history = []
        
        # Enhanced tracking
        self.start_time = datetime.now()
        self.total_pnl = 0.0
        self.win_count = 0
        self.loss_count = 0
        
        # Initialize based on platform
        self._initialize_for_platform()
        
        # AI Learning (if available)
        self.ai_enabled = False
        self._initialize_ai_learning()
    
    def _initialize_for_platform(self):
        """Initialize bot based on detected platform"""
        print(f"🔧 Initializing for {self.platform_info['os']} platform...")
        
        if self.platform_info['recommended_mode'] == 'offline':
            print("📱 Offline mode: Using simulated price data")
            self.current_eth_price = 3000.0
            self.price_history = [self.current_eth_price]
            self.volatility = 0.02
            self.trend = 0.001
            self.last_update = time.time()
        else:
            print("🌐 Online mode: Using real market data")
            self.current_eth_price = 3000.0
            self.last_valid_price = 3000.0
    
    def _initialize_ai_learning(self):
        """Initialize AI learning if available"""
        try:
            from ai_standalone import initialize_standalone_ai_learning
            initialize_standalone_ai_learning("simulation_data.json")
            self.ai_enabled = True
            print("🧠 AI Learning enabled")
        except Exception as e:
            print(f"⚠️ AI Learning not available: {e}")
            self.ai_enabled = False
    
    def get_eth_price(self) -> float:
        """Get ETH price with platform-appropriate fallbacks"""
        
        # Offline mode - simulate price
        if self.platform_info['recommended_mode'] == 'offline':
            return self._simulate_eth_price()
        
        # Online mode - try real APIs
        if self.platform_info['has_internet']:
            try:
                import requests
                
                # Try CoinGecko (most reliable)
                response = requests.get(
                    "https://api.coingecko.com/api/v3/simple/price",
                    params={"ids": "ethereum", "vs_currencies": "usd"},
                    timeout=10
                )
                if response.status_code == 200:
                    price = float(response.json()["ethereum"]["usd"])
                    self.last_valid_price = price
                    return price
            except Exception as e:
                print(f"CoinGecko failed: {e}")
            
            try:
                # Fallback to Binance
                response = requests.get(
                    "https://api.binance.com/api/v3/ticker/price",
                    params={"symbol": "ETHUSDT"},
                    timeout=10
                )
                if response.status_code == 200:
                    price = float(response.json()["price"])
                    self.last_valid_price = price
                    return price
            except Exception as e:
                print(f"Binance failed: {e}")
        
        # Use last valid price or fallback
        return getattr(self, 'last_valid_price', 3000.0)
    
    def _simulate_eth_price(self) -> float:
        """Simulate realistic ETH price movements for offline mode"""
        import random
        import math
        
        current_time = time.time()
        time_diff = current_time - getattr(self, 'last_update', current_time)
        
        # Random walk with trend and volatility
        random_change = random.gauss(0, self.volatility * math.sqrt(time_diff))
        trend_change = self.trend * time_diff
        
        # Apply changes
        self.current_eth_price *= (1 + random_change + trend_change)
        
        # Keep price reasonable
        self.current_eth_price = max(1000, min(10000, self.current_eth_price))
        
        self.price_history.append(self.current_eth_price)
        self.last_update = current_time
        
        # Keep only last 100 prices
        if len(self.price_history) > 100:
            self.price_history.pop(0)
        
        return self.current_eth_price
    
    def calculate_simple_indicators(self) -> Dict[str, float]:
        """Calculate simple technical indicators"""
        if len(self.price_history) < 10:
            return {'rsi': 50.0, 'trend': 0.0, 'volatility': 0.0}
        
        prices = self.price_history[-20:]  # Last 20 prices
        
        # Simple RSI calculation
        gains = []
        losses = []
        for i in range(1, len(prices)):
            change = prices[i] - prices[i-1]
            if change > 0:
                gains.append(change)
                losses.append(0)
            else:
                gains.append(0)
                losses.append(abs(change))
        
        avg_gain = sum(gains) / len(gains) if gains else 0
        avg_loss = sum(losses) / len(losses) if losses else 0
        
        if avg_loss == 0:
            rsi = 100
        else:
            rs = avg_gain / avg_loss
            rsi = 100 - (100 / (1 + rs))
        
        # Simple trend calculation
        if len(prices) >= 5:
            recent_avg = sum(prices[-5:]) / 5
            older_avg = sum(prices[-10:-5]) / 5 if len(prices) >= 10 else prices[0]
            trend = (recent_avg - older_avg) / older_avg
        else:
            trend = 0.0
        
        # Simple volatility calculation
        if len(prices) >= 2:
            returns = [(prices[i] - prices[i-1]) / prices[i-1] for i in range(1, len(prices))]
            volatility = sum(abs(r) for r in returns) / len(returns)
        else:
            volatility = 0.0
        
        return {
            'rsi': rsi,
            'trend': trend,
            'volatility': volatility
        }
    
    def generate_signal(self) -> Dict[str, Any]:
        """Generate trading signal using AI or simple logic"""
        
        # Try AI signal first
        if self.ai_enabled:
            try:
                from ai_standalone import get_standalone_ai_signal
                
                market_data = {
                    'price': self.current_eth_price,
                    'rsi': self.calculate_simple_indicators()['rsi'],
                    'volume_24h': 1000000.0,  # Placeholder
                    'funding_rate': 0.001
                }
                
                portfolio_data = {
                    'current_balance': self.balance,
                    'total_pnl': self.total_pnl,
                    'win_rate': self.win_count / (self.win_count + self.loss_count) if (self.win_count + self.loss_count) > 0 else 0.5,
                    'positions': self.positions,
                    'total_trades': len(self.trade_history)
                }
                
                ai_signal = get_standalone_ai_signal(market_data, self.trade_history, portfolio_data)
                
                return {
                    'action': ai_signal.action,
                    'confidence': ai_signal.confidence,
                    'reasoning': ai_signal.reasoning,
                    'source': 'AI'
                }
            except Exception as e:
                print(f"AI signal failed: {e}")
        
        # Fallback to simple signal logic
        indicators = self.calculate_simple_indicators()
        
        # Simple signal logic
        if indicators['rsi'] < 30 and indicators['trend'] > 0:
            action = 'long'
            confidence = 0.7
            reasoning = f"Oversold (RSI: {indicators['rsi']:.1f}) with upward trend"
        elif indicators['rsi'] > 70 and indicators['trend'] < 0:
            action = 'short'
            confidence = 0.7
            reasoning = f"Overbought (RSI: {indicators['rsi']:.1f}) with downward trend"
        else:
            action = 'hold'
            confidence = 0.5
            reasoning = f"Neutral conditions (RSI: {indicators['rsi']:.1f})"
        
        return {
            'action': action,
            'confidence': confidence,
            'reasoning': reasoning,
            'source': 'Simple'
        }
    
    def execute_trade(self, signal: Dict[str, Any]) -> bool:
        """Execute a trade based on signal"""
        if signal['action'] == 'hold':
            return False
        
        # Simple trade execution (simulated)
        trade_size = min(100.0, self.balance * 0.1)  # Max 10% of balance
        
        if signal['action'] == 'long':
            # Simulate long trade
            entry_price = self.current_eth_price
            # Simulate price movement
            exit_price = entry_price * (1 + 0.02 if signal['confidence'] > 0.6 else -0.01)
            pnl = trade_size * (exit_price - entry_price) / entry_price
            
            trade = {
                'id': f"trade_{int(time.time())}",
                'action': 'long',
                'entry_price': entry_price,
                'exit_price': exit_price,
                'size': trade_size,
                'pnl': pnl,
                'timestamp': datetime.now().isoformat(),
                'signal': signal
            }
            
        else:  # short
            # Simulate short trade
            entry_price = self.current_eth_price
            # Simulate price movement
            exit_price = entry_price * (1 - 0.02 if signal['confidence'] > 0.6 else 0.01)
            pnl = trade_size * (entry_price - exit_price) / entry_price
            
            trade = {
                'id': f"trade_{int(time.time())}",
                'action': 'short',
                'entry_price': entry_price,
                'exit_price': exit_price,
                'size': trade_size,
                'pnl': pnl,
                'timestamp': datetime.now().isoformat(),
                'signal': signal
            }
        
        # Update balance and history
        self.balance += pnl
        self.total_pnl += pnl
        self.trade_history.append(trade)
        
        # Update win/loss count
        if pnl > 0:
            self.win_count += 1
        else:
            self.loss_count += 1
        
        # Learn from outcome if AI is enabled
        if self.ai_enabled:
            try:
                from ai_standalone import learn_from_trade_standalone
                learn_from_trade_standalone(signal, trade)
            except:
                pass
        
        print(f"✅ Trade executed: {signal['action'].upper()} | PnL: ${pnl:.2f} | Balance: ${self.balance:.2f}")
        return True
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """Get comprehensive performance statistics"""
        runtime = (datetime.now() - self.start_time).total_seconds() / 3600  # hours
        
        total_trades = len(self.trade_history)
        win_rate = (self.win_count / total_trades * 100) if total_trades > 0 else 0
        
        return {
            'runtime_hours': runtime,
            'total_trades': total_trades,
            'win_count': self.win_count,
            'loss_count': self.loss_count,
            'win_rate': win_rate,
            'total_pnl': self.total_pnl,
            'current_balance': self.balance,
            'ai_enabled': self.ai_enabled,
            'platform_mode': self.platform_info['recommended_mode']
        }
    
    def display_status(self):
        """Display current bot status with enhanced information"""
        indicators = self.calculate_simple_indicators()
        stats = self.get_performance_stats()
        
        print(f"\n📊 Bot Status - Cycle {self.cycle_count}")
        print(f"💰 Balance: ${self.balance:,.2f}")
        print(f"📈 ETH Price: ${self.current_eth_price:,.2f}")
        print(f"📊 RSI: {indicators['rsi']:.1f}")
        print(f"📈 Trend: {indicators['trend']:.3f}")
        print(f"📊 Volatility: {indicators['volatility']:.3f}")
        print(f"🎯 Trades: {stats['total_trades']} (Wins: {stats['win_count']}, Losses: {stats['loss_count']})")
        print(f"📈 Win Rate: {stats['win_rate']:.1f}%")
        print(f"💰 Total PnL: ${stats['total_pnl']:,.2f}")
        print(f"⏱️ Runtime: {stats['runtime_hours']:.1f} hours")
        print(f"🧠 AI: {'Enabled' if self.ai_enabled else 'Disabled'}")
        print(f"🌐 Mode: {self.platform_info['recommended_mode'].title()}")
    
    def save_performance_data(self):
        """Save performance data to file"""
        try:
            stats = self.get_performance_stats()
            stats['last_update'] = datetime.now().isoformat()
            stats['trade_history'] = self.trade_history
            
            with open('bot_performance.json', 'w') as f:
                json.dump(stats, f, indent=2)
            print("💾 Performance data saved")
        except Exception as e:
            print(f"❌ Failed to save performance data: {e}")
    
    def trading_loop(self):
        """Main trading loop with enhanced features"""
        print("🔄 Starting trading loop...")
        
        while self.running:
            try:
                self.cycle_count += 1
                
                # Get current price
                self.current_eth_price = self.get_eth_price()
                
                # Display status every 10 cycles
                if self.cycle_count % 10 == 0:
                    self.display_status()
                
                # Save performance data every 50 cycles
                if self.cycle_count % 50 == 0:
                    self.save_performance_data()
                
                # Generate signal
                signal = self.generate_signal()
                
                # Execute trade if signal is strong enough
                if signal['confidence'] > 0.6:
                    self.execute_trade(signal)
                
                # Wait between cycles
                time.sleep(30)  # 30 seconds between cycles
                
            except KeyboardInterrupt:
                print("\n⏹️ Stopping bot...")
                break
            except Exception as e:
                print(f"❌ Error in trading loop: {e}")
                time.sleep(10)  # Wait before retrying
        
        # Save final performance data
        self.save_performance_data()
    
    def start(self):
        """Start the trading bot with enhanced startup"""
        print("🚀 Starting Unified Trading Bot v2.0")
        print(f"🖥️ Platform: {self.platform_info['os']}")
        print(f"📱 Mobile: {'Yes' if self.platform_info['is_mobile'] else 'No'}")
        print(f"🌐 Internet: {'Yes' if self.platform_info['has_internet'] else 'No'}")
        print(f"🎯 Mode: {self.platform_info['recommended_mode'].title()}")
        print(f"🧠 AI Learning: {'Enabled' if self.ai_enabled else 'Disabled'}")
        print(f"📊 Version: {self.platform_info['version']}")
        print("\n" + "="*50)
        
        self.running = True
        
        try:
            self.trading_loop()
        except KeyboardInterrupt:
            print("\n👋 Bot stopped by user")
        finally:
            self.running = False
            print("✅ Bot shutdown complete")
            self.display_status()

def main():
    """Main entry point - automatically detects platform and starts appropriate bot"""
    print("🤖 Unified Trading Bot v2.0 - All Platforms")
    print("=" * 50)
    
    # Detect platform
    platform_info = PlatformDetector.detect_platform()
    
    # Create and start bot
    bot = UnifiedTradingBot(platform_info)
    bot.start()

if __name__ == "__main__":
    main()