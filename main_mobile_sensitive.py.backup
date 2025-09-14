# main_mobile_sensitive.py - More sensitive signal detection

import time
import threading
from datetime import datetime
import requests
import json

class SensitiveMobileTradingBot:
    """
    Mobile trading bot with more sensitive signal detection
    """
    
    def __init__(self):
        self.running = False
        self.cycle_count = 0
        self.balance = 10000.0
        self.positions = []
        self.trade_history = []
        
    def get_eth_price_simple(self):
        """Get ETH price with fallback options for mobile"""
        try:
            # Try CoinGecko first (most reliable)
            response = requests.get(
                "https://api.coingecko.com/api/v3/simple/price",
                params={"ids": "ethereum", "vs_currencies": "usd"},
                timeout=10
            )
            if response.status_code == 200:
                return float(response.json()["ethereum"]["usd"])
        except Exception as e:
            print(f"CoinGecko failed: {e}")
        
        try:
            # Fallback to Jupiter
            response = requests.get(
                "https://price.jup.ag/v4/price",
                params={"ids": "7vfCXTUXx5WJV5JADk17DUJ4ksgau7utNKj4b963voxs"},
                timeout=10
            )
            if response.status_code == 200:
                data = response.json()
                if "data" in data and "7vfCXTUXx5WJV5JADk17DUJ4ksgau7utNKj4b963voxs" in data["data"]:
                    return float(data["data"]["7vfCXTUXx5WJV5JADk17DUJ4ksgau7utNKj4b963voxs"]["price"])
        except Exception as e:
            print(f"Jupiter failed: {e}")
        
        # Final fallback
        return 3000.0
    
    def sensitive_signal_detection(self):
        """More sensitive signal detection"""
        try:
            current_price = self.get_eth_price_simple()
            print(f"📊 Current ETH Price: ${current_price:,.2f}")
            
            # Initialize price history
            if not hasattr(self, 'price_history'):
                self.price_history = [current_price]
            else:
                self.price_history.append(current_price)
                
            # Keep only last 10 prices
            if len(self.price_history) > 10:
                self.price_history.pop(0)
            
            signals = []
            
            # 1. Simple momentum (MORE SENSITIVE - 0.3% instead of 1%)
            if len(self.price_history) >= 2:
                price_change = (current_price - self.price_history[-2]) / self.price_history[-2]
                
                if price_change > 0.003:  # 0.3% increase (was 1%)
                    signals.append({
                        'signal': 'long',
                        'confidence': min(abs(price_change) * 20, 3.0),
                        'reason': f'Price up {price_change:.2%}'
                    })
                elif price_change < -0.003:  # 0.3% decrease (was 1%)
                    signals.append({
                        'signal': 'short',
                        'confidence': min(abs(price_change) * 20, 3.0),
                        'reason': f'Price down {price_change:.2%}'
                    })
            
            # 2. Trend following (NEW - detects small trends)
            if len(self.price_history) >= 5:
                recent_avg = sum(self.price_history[-3:]) / 3
                older_avg = sum(self.price_history[-5:-2]) / 3
                
                if recent_avg > older_avg * 1.002:  # 0.2% trend
                    signals.append({
                        'signal': 'long',
                        'confidence': 1.5,
                        'reason': f'Uptrend detected ({recent_avg:.2f} vs {older_avg:.2f})'
                    })
                elif recent_avg < older_avg * 0.998:  # 0.2% trend
                    signals.append({
                        'signal': 'short',
                        'confidence': 1.5,
                        'reason': f'Downtrend detected ({recent_avg:.2f} vs {older_avg:.2f})'
                    })
            
            # 3. Volatility breakout (NEW - detects sudden moves)
            if len(self.price_history) >= 3:
                volatility = abs(current_price - self.price_history[-2]) / self.price_history[-2]
                if volatility > 0.005:  # 0.5% volatility
                    direction = 'long' if current_price > self.price_history[-2] else 'short'
                    signals.append({
                        'signal': direction,
                        'confidence': 1.8,
                        'reason': f'Volatility breakout {volatility:.2%}'
                    })
            
            # 4. Random signal generator (for testing - generates signals every few cycles)
            if self.cycle_count % 3 == 0:  # Every 3rd cycle
                import random
                if random.random() < 0.3:  # 30% chance
                    direction = random.choice(['long', 'short'])
                    signals.append({
                        'signal': direction,
                        'confidence': 1.2,
                        'reason': f'Random {direction} signal (testing)'
                    })
            
            # Return strongest signal
            if signals:
                best_signal = max(signals, key=lambda x: x['confidence'])
                return best_signal
            
            return {'signal': None, 'reason': 'No strong signals (market stable)'}
            
        except Exception as e:
            print(f"Signal detection error: {e}")
            return {'signal': None, 'reason': f'Error: {e}'}
    
    def execute_simulated_trade(self, signal_data):
        """Execute a simulated trade"""
        if not signal_data['signal']:
            return False
            
        trade_size = 100  # Fixed $100 trades
        current_price = self.get_eth_price_simple()
        
        print(f"\n💰 SIMULATED TRADE:")
        print(f"   Direction: {signal_data['signal'].upper()}")
        print(f"   Size: ${trade_size}")
        print(f"   Price: ${current_price:,.2f}")
        print(f"   Reason: {signal_data['reason']}")
        
        # Simulate trade execution
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
        """Update open positions"""
        if not self.positions:
            return
            
        current_price = self.get_eth_price_simple()
        
        for position in self.positions:
            if position['status'] != 'open':
                continue
                
            # Calculate PnL
            if position['side'] == 'long':
                pnl_pct = (current_price - position['entry_price']) / position['entry_price']
            else:
                pnl_pct = (position['entry_price'] - current_price) / position['entry_price']
            
            pnl_usd = position['size'] * pnl_pct
            
            # More sensitive take profit/stop loss
            if pnl_pct >= 0.01:  # 1% profit (was 2%)
                position['status'] = 'closed'
                position['exit_price'] = current_price
                position['exit_time'] = datetime.now().isoformat()
                position['pnl'] = pnl_usd
                self.balance += position['size'] + pnl_usd
                self.trade_history.append(position)
                print(f"🎯 Take profit hit: +${pnl_usd:.2f}")
                
            elif pnl_pct <= -0.005:  # 0.5% loss (was 1%)
                position['status'] = 'closed'
                position['exit_price'] = current_price
                position['exit_time'] = datetime.now().isoformat()
                position['pnl'] = pnl_usd
                self.balance += position['size'] + pnl_usd
                self.trade_history.append(position)
                print(f"🛑 Stop loss hit: ${pnl_usd:.2f}")
    
    def run_trading_cycle(self):
        """Run one trading cycle"""
        self.cycle_count += 1
        print(f"\n{'='*50}")
        print(f"📊 TRADING CYCLE #{self.cycle_count}")
        print(f"{'='*50}")
        
        # Update existing positions
        self.update_positions()
        
        # Show portfolio status
        open_positions = len([p for p in self.positions if p['status'] == 'open'])
        total_pnl = sum(p.get('pnl', 0) for p in self.trade_history)
        
        print(f"💰 Balance: ${self.balance:,.2f}")
        print(f"📈 Total PnL: ${total_pnl:,.2f}")
        print(f"🔓 Open Positions: {open_positions}")
        
        # Detect signals
        print("\n🔍 Detecting signals...")
        signal = self.sensitive_signal_detection()
        
        if signal['signal']:
            print(f"📡 Signal detected: {signal['signal'].upper()}")
            print(f"   Confidence: {signal['confidence']:.1f}")
            print(f"   Reason: {signal['reason']}")
            
            # Execute trade
            self.execute_simulated_trade(signal)
        else:
            print("📡 No signal detected")
        
        print(f"\n⏱️  Waiting 20 seconds...")
        time.sleep(20)  # Faster cycles for more action
    
    def start(self):
        """Start the sensitive mobile trading bot"""
        print("🚀 Starting Sensitive Mobile ETH Trading Bot")
        print("📱 More sensitive signal detection")
        print("🧪 DRY RUN MODE - No real money used")
        print(f"💰 Starting Balance: ${self.balance:,.2f}")
        print("\nPress Ctrl+C to stop\n")
        
        self.running = True
        
        try:
            while self.running:
                self.run_trading_cycle()
                
        except KeyboardInterrupt:
            print("\n\n🛑 Bot stopped by user")
            self.show_final_results()
        except Exception as e:
            print(f"\n❌ Error: {e}")
            self.show_final_results()
    
    def show_final_results(self):
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

def main():
    bot = SensitiveMobileTradingBot()
    bot.start()

if __name__ == "__main__":
    main()