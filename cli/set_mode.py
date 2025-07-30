from utils.config import load_config, save_config

def set_mode():
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
    SafeWalletManager.mode = selected
    print(f"✅ Mode set to: {selected}")
