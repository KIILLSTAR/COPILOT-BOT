# main_mobile_fixed.py - Complete fixed version with proper price history

import time
import threading
from datetime import datetime
import requests
import json

class FixedMobileTradingBot:
    """
    Complete mobile trading bot with proper price history and enhanced signal detection
    """
    
    def __init__(self):
        self.running = False
        self.cycle_count = 0
        self.balance = 10000.0
        self.positions = []
        self.trade_history = []
        self.price_history = []  # Initialize price history properly
        
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
                price = float(response.json()["ethereum"]["usd"])
                print(f"✅ CoinGecko price: ${price:,.2f}")
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
                print(f"✅ Binance price: ${price:,.2f}")
                self.last_valid_price = price
                return price
        except Exception as e:
            print(f"Binance failed: {e}")
        
        if hasattr(self, 'last_valid_price'):
            print(f"⚠️ Using last known price: ${self.last_valid_price:,.2f}")
            return self.last_valid_price
        print("⚠️ No price data available. Skipping this cycle.")
        return None
    
    def enhanced_signal_detection(self):
        """Enhanced signal detection with multiple strategies"""
        try:
            current_price = self.get_eth_price_simple()
            if current_price is None:
                print("⚠️ Skipping signal detection due to missing price.")
                return {'signal': None, 'reason': 'No price data'}
            
            # Add current price to history
            self.price_history.append(current_price)
            
            # Keep only last 20 prices
            if len(self.price_history) > 20:
                self.price_history.pop(0)
            
            # Show price history status
            print(f"📈 Price history: {len(self.price_history)} data points")
            
            signals = []
            
            # Wait for enough price data
            if len(self.price_history) < 3:
                return {'signal': None, 'reason': f'Building price history ({len(self.price_history)}/3)'}
            
            # 1. Simple momentum (compare current vs previous price)
            if len(self.price_history) >= 2:
                previous_price = self.price_history[-2]
                price_change = (current_price - previous_price) / previous_price
                
                print(f"📊 Price change: {price_change:+.2%}")
                
                if price_change > 0.003:  # 0.3% increase (more sensitive)
                    signals.append({
                        'signal': 'long',
                        'confidence': min(abs(price_change) * 20, 3.0),
                        'reason': f'Price up {price_change:.2%}'
                    })
                elif price_change < -0.003:  # 0.3% decrease (more sensitive)
                    signals.append({
                        'signal': 'short',
                        'confidence': min(abs(price_change) * 20, 3.0),
                        'reason': f'Price down {price_change:.2%}'
                    })
            
            # 2. Trend following (compare recent vs older prices)
            if len(self.price_history) >= 5:
                recent_avg = sum(self.price_history[-3:]) / 3
                older_avg = sum(self.price_history[-5:-2]) / 3
                
                trend_change = (recent_avg - older_avg) / older_avg
                print(f"📈 Trend change: {trend_change:+.2%}")
                
                if trend_change > 0.002:  # 0.2% uptrend (more sensitive)
                    signals.append({
                        'signal': 'long',
                        'confidence': 1.8,
                        'reason': f'Uptrend detected ({trend_change:.2%})'
                    })
                elif trend_change < -0.002:  # 0.2% downtrend (more sensitive)
                    signals.append({
                        'signal': 'short',
                        'confidence': 1.8,
                        'reason': f'Downtrend detected ({trend_change:.2%})'
                    })
            
            # 3. Volatility breakout
            if len(self.price_history) >= 3:
                volatility = abs(current_price - self.price_history[-2]) / self.price_history[-2]
                if volatility > 0.005:  # 0.5% volatility (more sensitive)
                    direction = 'long' if current_price > self.price_history[-2] else 'short'
                    signals.append({
                        'signal': direction,
                        'confidence': 2.0,
                        'reason': f'Volatility breakout {volatility:.2%}'
                    })
            
            # 4. RSI-like indicator
            if len(self.price_history) >= 8:
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
                
                avg_gain = sum(gains[-8:]) / 8 if gains else 0
                avg_loss = sum(losses[-8:]) / 8 if losses else 0
                
                rsi = 100 - (100 / (1 + (avg_gain / avg_loss))) if avg_loss > 0 else 50
                print(f"📊 RSI: {rsi:.1f}")
                
                if rsi < 35:  # More sensitive
                    signals.append({
                        'signal': 'long',
                        'confidence': 2.2,
                        'reason': f'RSI oversold ({rsi:.1f})'
                    })
                elif rsi > 65:  # More sensitive
                    signals.append({
                        'signal': 'short',
                        'confidence': 2.2,
                        'reason': f'RSI overbought ({rsi:.1f})'
                    })
            
            # 5. Random signals for testing (after 3 cycles)
            if self.cycle_count >= 3 and self.cycle_count % 3 == 0:
                import random
                if random.random() < 0.4:  # 40% chance (more frequent)
                    direction = random.choice(['long', 'short'])
                    signals.append({
                        'signal': direction,
                        'confidence': 1.5,
                        'reason': f'Random {direction} signal (cycle {self.cycle_count})'
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
            # Lowered thresholds for more frequent closes
            if pnl_pct >= 0.005:  # 0.5% profit
                position['status'] = 'closed'
                position['exit_price'] = current_price
                position['exit_time'] = datetime.now().isoformat()
                position['pnl'] = pnl_usd
                self.balance += position['size'] + pnl_usd
                self.trade_history.append(position)
                print(f"🎯 Take profit hit: +${pnl_usd:.2f}")
            elif pnl_pct <= -0.003:  # 0.3% loss
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
        signal = self.enhanced_signal_detection()
        
        if signal['signal']:
            print(f"📡 Signal detected: {signal['signal'].upper()}")
            print(f"   Confidence: {signal['confidence']:.1f}")
            print(f"   Reason: {signal['reason']}")
            
            # Execute trade
            self.execute_simulated_trade(signal)
        else:
            print(f"📡 {signal['reason']}")
        
        print(f"\n⏱️  Waiting 25 seconds...")
        time.sleep(25)  # Slightly faster cycles
    
    def start(self):
        """Start the fixed mobile trading bot"""
        print("🚀 Starting Enhanced Mobile ETH Trading Bot")
        print("📱 Complete with price history and multiple strategies")
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
    bot = FixedMobileTradingBot()
    bot.start()

if __name__ == "__main__":
    main()