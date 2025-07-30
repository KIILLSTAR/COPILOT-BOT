from solana.rpc.api import Client
from solana.keypair import Keypair
from safe_wallet_manager.safe_swap import safe_execute_swap
from safe_wallet_manager.config import DRY_RUN
from token_config import get_mint

# === CONFIG ===
RPC_URL = "https://api.mainnet-beta.solana.com"
PRIVATE_KEY = [INSERT_YOUR_PRIVATE_KEY_ARRAY]

# === INIT CLIENT & WALLET ===
client = Client(RPC_URL)
keypair = Keypair.from_secret_key(bytes(PRIVATE_KEY))
wallet_address = str(keypair.public_key)

# === STRATEGY LOGIC ===
def select_token(market_dipping: bool = False, manual_override: str = None):
    if manual_override:
        return get_mint(manual_override)
    return get_mint("USDC") if market_dipping else get_mint("ETH_PORTAL")

# === SWAP FUNCTION ===
def execute_swap(wallet_address, mint):
    if DRY_RUN:
        print(f"[DRY RUN] Would execute swap for {mint} from {wallet_address}")
        return "dry_run_tx_id"

    print(f"Executing live swap for {mint} from {wallet_address}")
    return "mock_tx_id_123"

# === RUN SWAP SAFELY ===
if __name__ == "__main__":
    print("🚀 COPILOT-BOT starting...")

    # Example: market dip detected
    market_dipping = True
    active_mint = select_token(market_dipping)

    # Or override manually:
    # active_mint = select_token(manual_override="SOL")

    safe_execute_swap(client, wallet_address, active_mint, execute_swap)
