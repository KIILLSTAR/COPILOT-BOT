#!/usr/bin/env python3
"""
Jupiter ETH Perps Trading Bot Setup
Guides you through secure configuration
"""
import os
import sys
import subprocess
from pathlib import Path

def check_python_version():
    """Ensure Python 3.8+ is installed"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ required. Current version:", sys.version)
        return False
    print(f"✅ Python {sys.version.split()[0]} detected")
    return True

def install_requirements():
    """Install required packages"""
    print("\n📦 Installing requirements...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Requirements installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install requirements: {e}")
        return False

def setup_environment():
    """Setup .env file"""
    print("\n🔧 Setting up environment configuration...")
    
    if os.path.exists('.env'):
        print("⚠️  .env file already exists. Backup created as .env.backup")
        os.rename('.env', '.env.backup')
    
    # Copy template
    if os.path.exists('.env.example'):
        print("📋 Creating .env from template...")
        with open('.env.example', 'r') as src, open('.env', 'w') as dst:
            dst.write(src.read())
        print("✅ .env file created")
        print("\n🚨 IMPORTANT: Edit .env file with your actual values:")
        print("   - Add your Solana wallet private key")
        print("   - Verify RPC endpoint")
        print("   - Adjust trading parameters")
        return True
    else:
        print("❌ .env.example not found")
        return False

def verify_setup():
    """Test the configuration"""
    print("\n🧪 Testing configuration...")
    try:
        from wallet.secure_wallet import wallet_manager
        if wallet_manager.is_ready():
            balance = wallet_manager.get_balance()
            print(f"✅ Wallet connected. SOL balance: {balance:.4f}")
            return True
        else:
            print("❌ Wallet not ready. Check your .env configuration")
            return False
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False

def main():
    """Main setup process"""
    print("🚀 Jupiter ETH Perps Trading Bot Setup")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        return False
    
    # Install requirements
    if not install_requirements():
        return False
    
    # Setup environment
    if not setup_environment():
        return False
    
    print("\n" + "=" * 50)
    print("✅ Setup complete!")
    print("\n📝 Next steps:")
    print("1. Edit .env file with your wallet credentials")
    print("2. Run: python3 setup.py --test")
    print("3. Start trading: python3 main.py")
    print("\n⚠️  SECURITY REMINDER:")
    print("   - Never share your private key")
    print("   - Never commit .env to version control")
    print("   - Start with small trade sizes")
    
    return True

if __name__ == "__main__":
    if "--test" in sys.argv:
        verify_setup()
    else:
        main()