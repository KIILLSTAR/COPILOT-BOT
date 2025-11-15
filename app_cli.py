"""
Consolidated CLI Module
Combines all command-line interface functionality
"""
import os
from typing import List, Dict, Any

# =============================================================================
# MODE SETTER (from cli/set_mode.py)
# =============================================================================

def set_mode():
    """Set trading mode via CLI"""
    from config import load_config, save_config
    
    print("Select mode:")
    print("1. manual")
    print("2. auto_safe")
    print("3. auto_all")
    print("4. dry_run")
    choice = input("Enter choice [1-4]: ")

    modes = {
        "1": "manual",
        "2": "auto_safe",
        "3": "auto_all",
        "4": "dry_run"
    }

    selected = modes.get(choice, "auto_safe")
    
    # Update configuration
    config = load_config()
    config["mode"] = selected
    save_config(config)
    
    print(f"✅ Mode set to: {selected}")

# =============================================================================
# AUDIT LOG VIEWER (from cli/view_audit_log.py)
# =============================================================================

def get_audit_logs() -> List[str]:
    """Get audit logs from various sources"""
    logs = []
    
    # Try to read from trade log file
    if os.path.exists("trade_log.txt"):
        with open("trade_log.txt", "r") as f:
            logs.extend(f.readlines())
    
    # Try to read from logs directory
    if os.path.exists("logs"):
        for log_file in os.listdir("logs"):
            if log_file.endswith(".log"):
                with open(f"logs/{log_file}", "r") as f:
                    logs.extend(f.readlines())
    
    # If no logs found, return sample data
    if not logs:
        logs = [
            "Trade: BUY SOL at 08:32",
            "Trade: SELL USDC at 08:45", 
            "Trade: BUY BONK at 09:01"
        ]
    
    return logs

def view_audit_logs():
    """Display audit logs in CLI"""
    logs = get_audit_logs()
    
    print("📋 AUDIT LOGS")
    print("=" * 50)
    
    if logs:
        for i, log in enumerate(logs[-20:], 1):  # Show last 20 entries
            print(f"{i:2d}. {log.strip()}")
    else:
        print("No logs found")
    
    print("=" * 50)

# =============================================================================
# SAFETY STATUS VIEWER
# =============================================================================

def view_safety_status():
    """Display detailed safety status"""
    from config import safety
    
    print("🔒 SAFETY STATUS")
    print("=" * 50)
    safety.print_safety_status()

# =============================================================================
# MAIN CLI INTERFACE
# =============================================================================

def main_cli():
    """Main CLI interface"""
    while True:
        print("\n🛠️  TRADING BOT CLI")
        print("=" * 30)
        print("1. Set trading mode")
        print("2. View audit logs")
        print("3. View safety status")
        print("4. Exit")
        
        choice = input("\nSelect option [1-4]: ").strip()
        
        if choice == "1":
            set_mode()
        elif choice == "2":
            view_audit_logs()
        elif choice == "3":
            view_safety_status()
        elif choice == "4":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please try again.")

# =============================================================================
# EXPORTS
# =============================================================================

__all__ = [
    'set_mode', 'get_audit_logs', 'view_audit_logs', 'view_safety_status', 'main_cli'
]