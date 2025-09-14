# main_offline.py - Completely offline trading bot for mobile

import time
import random
import math
from datetime import datetime

class OfflineTradingBot:
    """
    Completely offline trading bot that simulates ETH price movements
    Perfect for mobile devices with connectivity issues
    """
    
    def __init__(self):
        self.running = False
        self.cycle_count = 0
        self.balance = 10000.0
        self.positions = []
        self.trade_history = []
        
        # Simulated ETH price starting at $3000
        self.current_eth_price = 3000.0
        self.price_history = [self.current_eth_price]
        
        # Market simulation parameters
        self.volatility = 0.02  # 2% volatility
        self.trend = 0.001      # Slight upward trend
        self.last_update = time.time()
    
    def simulate_eth_price(self):
        """Simulate realistic ETH price movements"""
        current_time = time.time()
        time_diff = current_time - self.last_update
        
        # Random walk with trend and volatility
        random_change = random.gauss(0, self.volatility * math.sqrt(time_diff))
        trend_change = self.trend * time_diff
        
        # Apply changes
        self.current_eth_price *= (1 + random_change + trend_change)
        
        # Keep price reasonable (between $1000 and $10000)
        self.current_eth_price = max(1000, min(10000, self.current_eth_price))
        
        self.price_history.append(self.current_eth_price)
        self.last_update = current_time
        
        # Keep only last 100 prices
        if len(self.price_history) > 100:
            self.price_history.pop(0)
        
        return self.current_eth_price
    
    def calculate_technical_indicators(self):
        """Calculate simple technical indicators from price history"""
        if len(self.price_history) < 10:
            return {}
        
        # Simple moving averages
        sma_5 = sum(self.price_history[-5:]) / 5
        sma_10 = sum(self.price_history[-10:]) / 10
        
        # RSI-like indicator
        gains = []
        losses = []
        for i in range(1, len(self.price_history)):
            change = self.price_history[i] - self.price_history[i-1]
            if change > 0:
                gains.append(change)
                losses.append(0)
            else:
                gains.append(0)
                losses.append(abs(change))
        
        avg_gain = sum(gains[-14:]) / 14 if gains else 0
        avg_loss = sum(losses[-14:]) / 14 if losses else 0
        
        rsi = 100 - (100 / (1 + (avg_gain / avg_loss))) if avg_loss > 0 else 50
        
        return {
            'sma_5': sma_5,
            'sma_10': sma_10,
            'rsi': rsi,
            'price': self.current_eth_price
        }
    
    def detect_signals(self):
        """Detect trading signals using technical analysis"""
        indicators = self.calculate_technical_indicators()
        
        if not indicators:
            return {'signal': None, 'reason': 'Insufficient data'}
        
        signals = []
        
        # Moving average crossover
        if indicators['sma_5'] > indicators['sma_10']:
            signals.append({
                'signal': 'long',
                'confidence': 1.5,
                'reason': 'SMA crossover bullish'
            })
        elif indicators['sma_5'] < indicators['sma_10']:
            signals.append({
                'signal': 'short',
                'confidence': 1.5,
                'reason': 'SMA crossover bearish'
            })
        
        # RSI signals
        if indicators['rsi'] < 30:
            signals.append({
                'signal': 'long',
                'confidence': 2.0,
                'reason': f'RSI oversold ({indicators["rsi"]:.1f})'
            })
        elif indicators['rsi'] > 70:
            signals.append({
                'signal': 'short',
                'confidence': 2.0,
                'reason': f'RSI overbought ({indicators["rsi"]:.1f})'
            })
        
        # Momentum signals
        if len(self.price_history) >= 3:
            recent_change = (self.price_history[-1] - self.price_history[-3]) / self.price_history[-3]
            
            if recent_change > 0.03:  # 3% increase
                signals.append({
                    'signal': 'long',
                    'confidence': 1.8,
                    'reason': f'Strong momentum up {recent_change:.1%}'
                })
            elif recent_change < -0.03:  # 3% decrease
                signals.append({
                    'signal': 'short',
                    'confidence': 1.8,
                    'reason': f'Strong momentum down {recent_change:.1%}'
                })
        
        # Aggregate signals
        if not signals:
            return {'signal': None, 'reason': 'No clear signals'}
        
        # Find strongest signal
        best_signal = max(signals, key=lambda x: x['confidence'])
        
        # Only trade if confidence is high enough
        if best_signal['confidence'] >= 1.5:
            return best_signal
        
        return {'signal': None, 'reason': 'Weak signals'}
    
    def execute_trade(self, signal_data):
        """Execute a simulated trade"""
        if not signal_data['signal']:
            return False
        
        trade_size = 100  # Fixed $100 trades
        current_price = self.current_eth_price
        
        print(f"\n💰 SIMULATED TRADE:")
        print(f"   Direction: {signal_data['signal'].upper()}")
        print(f"   Size: ${trade_size}")
        print(f"   Price: ${current_price:,.2f}")
        print(f"   Reason: {signal_data['reason']}")
        
        # Create position
        position = {
            'id': f"pos_{int(time.time())}",
            'side': signal_data['signal'],
            'size': trade_size,
            'entry_price': current_price,
            'entry_time': datetime.now().isoformat(),
            'status': 'open'
        }
        
        self.positions.append(position)
        print(f"✅ Position opened: {position['id']}")
        return True
    
    def update_positions(self):
        """Update open positions with current simulated price"""
        if not self.positions:
            return
        
        for position in self.positions:
            if position['status'] != 'open':
                continue
            
            # Calculate PnL
            if position['side'] == 'long':
                pnl_pct = (self.current_eth_price - position['entry_price']) / position['entry_price']
            else:
                pnl_pct = (position['entry_price'] - self.current_eth_price) / position['entry_price']
            
            pnl_usd = position['size'] * pnl_pct
            
            # Take profit at 2% gain
            if pnl_pct >= 0.02:
                position['status'] = 'closed'
                position['exit_price'] = self.current_eth_price
                position['exit_time'] = datetime.now().isoformat()
                position['pnl'] = pnl_usd
                self.balance += position['size'] + pnl_usd
                self.trade_history.append(position)
                print(f"🎯 Take profit hit: +${pnl_usd:.2f}")
                
            # Stop loss at 1% loss
            elif pnl_pct <= -0.01:
                position['status'] = 'closed'
                position['exit_price'] = self.current_eth_price
                position['exit_time'] = datetime.now().isoformat()
                position['pnl'] = pnl_usd
                self.balance += position['size'] + pnl_usd
                self.trade_history.append(position)
                print(f"🛑 Stop loss hit: ${pnl_usd:.2f}")
    
    def run_cycle(self):
        """Run one trading cycle"""
        self.cycle_count += 1
        
        # Update simulated ETH price
        self.simulate_eth_price()
        
        print(f"\n{'='*50}")
        print(f"📊 TRADING CYCLE #{self.cycle_count}")
        print(f"{'='*50}")
        
        # Show current status
        indicators = self.calculate_technical_indicators()
        open_positions = len([p for p in self.positions if p['status'] == 'open'])
        total_pnl = sum(p.get('pnl', 0) for p in self.trade_history)
        
        print(f"💰 Balance: ${self.balance:,.2f}")
        print(f"📈 Total PnL: ${total_pnl:,.2f}")
        print(f"🔓 Open Positions: {open_positions}")
        print(f"📊 ETH Price: ${self.current_eth_price:,.2f}")
        print(f"📈 RSI: {indicators.get('rsi', 0):.1f}")
        
        # Update positions
        self.update_positions()
        
        # Detect and execute signals
        print("\n🔍 Detecting signals...")
        signal = self.detect_signals()
        
        if signal['signal']:
            print(f"📡 Signal detected: {signal['signal'].upper()}")
            print(f"   Confidence: {signal['confidence']:.1f}")
            print(f"   Reason: {signal['reason']}")
            
            # Execute trade (with some randomness to make it realistic)
            if random.random() < 0.7:  # 70% chance to execute
                self.execute_trade(signal)
            else:
                print("⏸️  Signal ignored (random chance)")
        else:
            print("📡 No signal detected")
        
        print(f"\n⏱️  Waiting 15 seconds...")
        time.sleep(15)  # Short cycle for mobile
    
    def start(self):
        """Start the offline trading bot"""
        print("🚀 Starting Offline ETH Trading Bot")
        print("📱 Mobile-optimized - No internet required")
        print("🧪 DRY RUN MODE - Simulated trading only")
        print(f"💰 Starting Balance: ${self.balance:,.2f}")
        print(f"📊 Starting ETH Price: ${self.current_eth_price:,.2f}")
        print("\nPress Ctrl+C to stop\n")
        
        self.running = True
        
        try:
            while self.running:
                self.run_cycle()
                
        except KeyboardInterrupt:
            print("\n\n🛑 Bot stopped by user")
            self.show_results()
        except Exception as e:
            print(f"\n❌ Error: {e}")
            self.show_results()
    
    def show_results(self):
        """Show final trading results"""
        total_trades = len(self.trade_history)
        winning_trades = len([t for t in self.trade_history if t.get('pnl', 0) > 0])
        total_pnl = sum(t.get('pnl', 0) for t in self.trade_history)
        win_rate = (winning_trades / total_trades * 100) if total_trades > 0 else 0
        
        print(f"\n📊 FINAL RESULTS:")
        print(f"   Starting Balance: $10,000.00")
        print(f"   Final Balance: ${self.balance:,.2f}")
        print(f"   Total PnL: ${total_pnl:,.2f}")
        print(f"   Total Trades: {total_trades}")
        print(f"   Win Rate: {win_rate:.1f}%")
        print(f"   ROI: {(total_pnl / 10000) * 100:.2f}%")
        print(f"   Final ETH Price: ${self.current_eth_price:,.2f}")

def main():
    bot = OfflineTradingBot()
    bot.start()

if __name__ == "__main__":
    main()