#!/usr/bin/env python3
"""
Cleanup Script - Remove Redundant Main Files
Safely removes duplicate main files after creating unified system
"""
import os
import shutil
from datetime import datetime

def backup_file(filepath):
    """Create a backup of a file before deletion"""
    if os.path.exists(filepath):
        backup_path = f"{filepath}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        shutil.copy2(filepath, backup_path)
        print(f"📦 Backed up: {filepath} -> {backup_path}")
        return backup_path
    return None

def cleanup_redundant_files():
    """Remove redundant main files safely"""
    print("🧹 Cleaning up redundant main files...")
    print("=" * 50)
    
    # List of redundant main files to remove
    redundant_files = [
        'main_minimal.py',
        'main_mobile.py', 
        'main_mobile_fixed.py',
        'main_mobile_sensitive.py',
        'main_offline.py',
        'main_simple.py',
        'unified_main.py',  # This is now the main.py
        'main_new.py'       # This was just for testing
    ]
    
    # Files to keep
    keep_files = [
        'main.py',           # The new unified main
        'main_old_backup.py' # Backup of original main
    ]
    
    removed_count = 0
    backed_up_count = 0
    
    for file in redundant_files:
        if os.path.exists(file):
            # Create backup first
            backup_path = backup_file(file)
            if backup_path:
                backed_up_count += 1
            
            # Remove the file
            os.remove(file)
            print(f"🗑️ Removed: {file}")
            removed_count += 1
        else:
            print(f"⚠️ Not found: {file}")
    
    print("\n" + "=" * 50)
    print(f"📊 Cleanup Summary:")
    print(f"   Files removed: {removed_count}")
    print(f"   Files backed up: {backed_up_count}")
    print(f"   Files kept: {len(keep_files)}")
    
    print(f"\n✅ Cleanup complete!")
    print(f"📁 Your main files are now:")
    for file in keep_files:
        if os.path.exists(file):
            print(f"   ✅ {file}")
        else:
            print(f"   ❌ {file} (missing)")

def show_new_structure():
    """Show the new simplified file structure"""
    print("\n" + "=" * 50)
    print("📁 NEW SIMPLIFIED STRUCTURE")
    print("=" * 50)
    
    print("""
🎯 MAIN FILES (Only 1 needed now!):
   main.py                    # ← The ONLY main file you need!

🔧 CORE MODULES (Consolidated):
   app_config.py              # All configuration
   app_logger.py              # All logging
   app_dashboard.py           # All dashboards
   app_core_trading.py        # Trading functions
   app_cli.py                 # Command line interface
   app_safe_wallet.py         # Wallet management

🧠 AI LEARNING:
   ai_standalone.py           # AI learning system
   ai_learning.py             # Advanced AI (optional)
   ai_signal_detector.py      # AI signal detection

📊 DATA & CONFIG:
   simulation_data.json       # Your trading data
   requirements.txt           # Dependencies
   README.md                  # Documentation

🎮 HOW TO USE:
   python main.py             # ← That's it! Works everywhere!
""")

def main():
    """Main cleanup function"""
    print("🤖 Trading Bot Cleanup Tool")
    print("Removing redundant main files...")
    
    # Ask for confirmation
    response = input("\n❓ Remove redundant main files? (y/N): ").lower().strip()
    
    if response == 'y':
        cleanup_redundant_files()
        show_new_structure()
        
        print("\n🎉 SUCCESS!")
        print("Your trading bot is now unified and simplified!")
        print("Just run: python main.py")
        
    else:
        print("❌ Cleanup cancelled")
        print("Files remain unchanged")

if __name__ == "__main__":
    main()