# main_simple.py - Simplified main file without complex dependencies

import time
from datetime import datetime

def main():
    print("🚀 Starting Simplified ETH Trading Bot")
    print("📱 Using mobile-optimized version")
    print("🧪 DRY RUN MODE - No real money used")
    
    try:
        # Import and run the mobile bot
        from main_mobile_fixed import FixedMobileTradingBot
        
        bot = FixedMobileTradingBot()
        bot.start()
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("\n🔧 Trying to install dependencies...")
        
        try:
            import subprocess
            import sys
            
            packages = ["requests", "pandas", "numpy"]
            for package in packages:
                print(f"Installing {package}...")
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            
            print("✅ Dependencies installed. Trying again...")
            from main_mobile_fixed import FixedMobileTradingBot
            bot = FixedMobileTradingBot()
            bot.start()
            
        except Exception as e2:
            print(f"❌ Setup failed: {e2}")
            print("\n📱 Alternative: Try running directly:")
            print("python main_mobile_fixed.py")
    
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\n📱 Try running the mobile bot directly:")
        print("python main_mobile_fixed.py")

if __name__ == "__main__":
    main()