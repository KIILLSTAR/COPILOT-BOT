#!/usr/bin/env python3
"""
Unified Trading Bot - Main Entry Point
Replaces all the old main files with one smart, adaptive system
"""
import sys
import os

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    """Main entry point - automatically detects platform and starts appropriate bot"""
    print("🚀 Starting Unified Trading Bot...")
    print("📱 Automatically adapting to your platform...")
    
    try:
        # Import and run the unified bot
        from unified_main import main as unified_main
        unified_main()
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("\n🔧 Trying fallback mode...")
        
        # Fallback to simple mode
        try:
            from main_simple import main as simple_main
            simple_main()
        except Exception as e2:
            print(f"❌ Fallback failed: {e2}")
            print("\n📱 Manual start options:")
            print("1. python unified_main.py")
            print("2. python main_simple.py")
            print("3. python main_offline.py")
    
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        print("\n🆘 Emergency fallback - try running:")
        print("python main_offline.py")

if __name__ == "__main__":
    main()