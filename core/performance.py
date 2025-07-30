# performance.py

def evaluate_performance():
    try:
        with open("trade_log.txt", "r") as f:
            trades = f.readlines()
        print(f"[PERFORMANCE] Total trades: {len(trades)}")
    except FileNotFoundError:
        print("[PERFORMANCE] No trades logged yet.")
