#!/usr/bin/env python3
"""
Simple setup script for the ETH Trading Bot
Handles dependencies and environment setup
"""

import subprocess
import sys
import os

def install_dependencies():
    """Install required packages"""
    print("📦 Installing dependencies...")
    
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

def test_imports():
    """Test that all imports work"""
    print("\n🧪 Testing imports...")
    
    imports = [
        "requests",
        "pandas", 
        "numpy",
        "solana",
        "base58"
    ]
    
    for module in imports:
        try:
            __import__(module)
            print(f"   ✅ {module} imported successfully")
        except ImportError as e:
            print(f"   ❌ Failed to import {module}: {e}")
            return False
    
    return True

def main():
    """Main setup function"""
    print("🚀 ETH Trading Bot Setup")
    print("=" * 40)
    
    # Install dependencies
    if not install_dependencies():
        print("\n❌ Setup failed during dependency installation")
        return False
    
    # Test imports
    if not test_imports():
        print("\n❌ Setup failed during import testing")
        return False
    
    print("\n🎉 Setup Complete!")
    print("=" * 40)
    print("\n📱 Next Steps:")
    print("1. Run: python main_mobile_fixed.py")
    print("2. Or try: python main_minimal.py")
    print("3. Or try: python main.py")
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)