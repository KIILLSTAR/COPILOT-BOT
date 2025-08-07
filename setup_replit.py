#!/usr/bin/env python3
"""
Replit Setup Script
Automatically configures the trading bot environment
"""

import os
import sys
import subprocess
import time

def print_banner():
    """Print setup banner"""
    print("🚀 ETH Trading Bot - Replit Setup")
    print("=" * 50)

def check_python_version():
    """Check Python version"""
    version = sys.version_info
    print(f"🐍 Python Version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ required")
        return False
    
    print("✅ Python version OK")
    return True

def install_dependencies():
    """Install required packages"""
    print("\n📦 Installing dependencies...")
    
    packages = [
        "requests>=2.25.0",
        "pandas>=1.3.0", 
        "numpy>=1.21.0",
        "solana>=0.36.0",
        "base58>=2.0.0"
    ]
    
    for package in packages:
        try:
            print(f"   Installing {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"   ✅ {package} installed")
        except subprocess.CalledProcessError as e:
            print(f"   ❌ Failed to install {package}: {e}")
            return False
    
    return True

def create_directories():
    """Create necessary directories"""
    print("\n📁 Creating directories...")
    
    directories = ["logs", "data", "config"]
    
    for directory in directories:
        try:
            os.makedirs(directory, exist_ok=True)
            print(f"   ✅ Created {directory}/")
        except Exception as e:
            print(f"   ❌ Failed to create {directory}/: {e}")
            return False
    
    return True

def test_imports():
    """Test that all imports work"""
    print("\n🧪 Testing imports...")
    
    imports = [
        ("requests", "requests"),
        ("pandas", "pd"),
        ("numpy", "np"),
        ("solana", "solana"),
        ("base58", "base58")
    ]
    
    for module, alias in imports:
        try:
            __import__(module)
            print(f"   ✅ {module} imported successfully")
        except ImportError as e:
            print(f"   ❌ Failed to import {module}: {e}")
            return False
    
    return True

def test_bot():
    """Test the offline bot briefly"""
    print("\n🤖 Testing bot functionality...")
    
    try:
        # Import and test the offline bot
        from main_offline import OfflineTradingBot
        
        bot = OfflineTradingBot()
        print("   ✅ Bot class created successfully")
        
        # Test price simulation
        price = bot.simulate_eth_price()
        print(f"   ✅ Price simulation: ${price:,.2f}")
        
        # Test signal detection
        signal = bot.detect_signals()
        print(f"   ✅ Signal detection: {signal.get('signal', 'None')}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Bot test failed: {e}")
        return False

def show_next_steps():
    """Show next steps for the user"""
    print("\n🎉 Setup Complete!")
    print("=" * 50)
    print("\n📱 Next Steps:")
    print("1. Click the 'Run' button to start the bot")
    print("2. The bot will run in offline mode by default")
    print("3. Monitor the console for trading activity")
    print("4. Press Ctrl+C to stop the bot")
    
    print("\n🔧 Available Modes:")
    print("- Offline Mode (default): python main_offline.py")
    print("- Mobile Mode: python main_mobile.py") 
    print("- Full Mode: python main.py")
    
    print("\n📊 Features:")
    print("- Realistic ETH price simulation")
    print("- Technical analysis signals")
    print("- Risk management (stop-loss/take-profit)")
    print("- Portfolio tracking")
    print("- Dry run mode (no real money)")
    
    print("\n🚀 Ready to trade!")

def main():
    """Main setup function"""
    print_banner()
    
    # Check Python version
    if not check_python_version():
        return False
    
    # Install dependencies
    if not install_dependencies():
        return False
    
    # Create directories
    if not create_directories():
        return False
    
    # Test imports
    if not test_imports():
        return False
    
    # Test bot
    if not test_bot():
        return False
    
    # Show next steps
    show_next_steps()
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        print("\n❌ Setup failed. Please check the errors above.")
        sys.exit(1)