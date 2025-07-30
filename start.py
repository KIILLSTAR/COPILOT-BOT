# start.py

import subprocess
import sys

def run_bot():
    subprocess.run(["python", "bot/main.py"])

def run_cli_dashboard():
    subprocess.run(["python", "dashboard/cli.py"])

def run_web_dashboard():
    subprocess.run(["python", "dashboard/web.py"])

def menu():
    print("\n🚀 COPILOT-BOT Launcher")
    print("1. Run Trading Bot")
    print("2. Launch CLI Dashboard")
    print("3. Launch Web Dashboard")
    print("4. Exit")

    choice = input("Select an option (1-4): ")

    if choice == "1":
        run_bot()
    elif choice == "2":
        run_cli_dashboard()
    elif choice == "3":
        run_web_dashboard()
    elif choice == "4":
        sys.exit()
    else:
        print("❌ Invalid choice. Try again.")
        menu()

if __name__ == "__main__":
    menu()
