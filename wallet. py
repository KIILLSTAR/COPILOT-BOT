# wallet.py

from solana.keypair import Keypair
from solana.publickey import PublicKey
import base64

def load_keypair(secret_key: str) -> Keypair:
    secret_bytes = base64.b64decode(secret_key)
    return Keypair.from_secret_key(secret_bytes)

def get_wallet_address(keypair: Keypair) -> str:
    return str(keypair.public_key)
