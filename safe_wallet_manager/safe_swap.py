import time
from safe_wallet_manager.config import MIN_BALANCE_THRESHOLD, LOG_PATH
from safe_wallet_manager.transfer_logger import log_transfer

def safe_execute_swap(client, wallet_address, mint, execute_swap_fn):
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Starting swap for {mint}")
    
    try:
        balance = client.get_balance(wallet_address)['result']['value'] / 1e9
        print(f"Wallet balance: {balance:.6f} SOL")

        if balance < MIN_BALANCE_THRESHOLD:
            print("⚠️ Balance too low — aborting swap.")
            return

        tx_id = execute_swap_fn(wallet_address, mint)
        print(f"✅ Swap executed. Transaction ID: {tx_id}")
        log_transfer(wallet_address, "DEX_SWAP", balance, tx_id)

    except Exception as e:
        print(f"❌ Swap failed: {e}")
