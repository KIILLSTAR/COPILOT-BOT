# logger.py

import datetime

def log_trade(signal, asset, amount):
    timestamp = datetime.datetime.now().isoformat()
    with open("trade_log.txt", "a") as f:
        f.write(f"{timestamp} | {signal} | {asset} | {amount}\n")
    print(f"[LOGGED] {signal} {amount} {asset} at {timestamp}")
