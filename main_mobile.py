# main_mobile.py - Mobile-optimized version of the trading bot

import time
import threading
from datetime import datetime
import requests
from core.price_fetcher import price_fetcher
import json

class MobileTradingBot:
    """
    Simplified trading bot optimized for mobile devices
    """
    
    def __init__(self):
        self.running = False
        self.cycle_count = 0
        self.balance = 10000.0
        self.positions = []
        self.trade_history = []
        
    def get_eth_price_simple(self):
        """Get ETH price using resilient multi-source fetcher."""
        return price_fetcher.get_eth_price()
    
    def simple_signal_detection(self):
        """Simplified signal detection for mobile"""
        try:
            current_price = self.get_eth_price_simple()
            print(f"📊 Current ETH Price: ${current_price:,.2f}")
            
            # Simple momentum-based signal
            if hasattr(self, 'last_price'):
                price_change = (current_price - self.last_price) / self.last_price
                
                if price_change > 0.01:  # 1% increase
                    return {
                        'signal': 'long',
                        'confidence': min(abs(price_change) * 10, 3.0),
                        'reason': f'Price up {price_change:.2%}'
                    }
                elif price_change < -0.01:  # 1% decrease
                    return {
                        'signal': 'short',
                        'confidence': min(abs(price_change) * 10, 3.0),
                        'reason': f'Price down {price_change:.2%}'
                    }
            
            self.last_price = current_price
            return {'signal': None, 'reason': 'No strong signal'}
            
        except Exception as e:
            print(f"Signal detection error: {e}")
            return {'signal': None, 'reason': f'Error: {e}'}
    
    def execute_simulated_trade(self, signal_data):
        """Execute a simulated trade"""
        if not signal_data['signal']:
            return False
            
        trade_size = 100  # Fixed $100 trades for mobile
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
            
            # Simple take profit/stop loss
            if pnl_pct >= 0.02:  # 2% profit
                position['status'] = 'closed'
                position['exit_price'] = current_price
                position['exit_time'] = datetime.now().isoformat()
                position['pnl'] = pnl_usd
                self.balance += position['size'] + pnl_usd
                self.trade_history.append(position)
                print(f"🎯 Take profit hit: +${pnl_usd:.2f}")
                
            elif pnl_pct <= -0.01:  # 1% loss
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
        print(f"\n{'='*40}")
        print(f"📊 TRADING CYCLE #{self.cycle_count}")
        print(f"{'='*40}")
        
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
        signal = self.simple_signal_detection()
        
        if signal['signal']:
            print(f"📡 Signal detected: {signal['signal'].upper()}")
            print(f"   Confidence: {signal['confidence']:.1f}")
            print(f"   Reason: {signal['reason']}")
            
            # Execute trade
            self.execute_simulated_trade(signal)
        else:
            print("📡 No signal detected")
        
        print(f"\n⏱️  Waiting 30 seconds...")
        time.sleep(30)  # Shorter cycle for mobile
    
    def start(self):
        """Start the mobile trading bot"""
        print("🚀 Starting Mobile ETH Trading Bot")
        print("📱 Optimized for mobile devices")
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
    bot = MobileTradingBot()
    bot.start()

if __name__ == "__main__":
    main()