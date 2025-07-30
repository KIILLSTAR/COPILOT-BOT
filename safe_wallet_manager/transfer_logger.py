from safe_wallet_manager.config import LOG_PATH

def log_transfer(wallet, recipient, amount, tx_id):
    with open(f"{LOG_PATH}transfer_log.txt", "a") as f:
        f.write(f"{wallet} → {recipient} | {amount:.6f} SOL | tx: {tx_id}\n")
