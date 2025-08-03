"""
Secure Wallet Management
Loads wallet credentials securely from environment variables
"""
import os
from typing import Optional
from solana.keypair import Keypair
from solana.publickey import PublicKey
from solana.rpc.api import Client
from dotenv import load_dotenv
import base58

# Load environment variables
load_dotenv()

class SecureWalletManager:
    """
    Secure wallet management using environment variables
    """
    
    def __init__(self):
        self.client = None
        self.keypair = None
        self.public_key = None
        self._initialize_wallet()
    
    def _initialize_wallet(self):
        """Initialize wallet from environment variables"""
        try:
            # Load RPC endpoint
            rpc_url = os.getenv('SOLANA_RPC_URL', 'https://api.mainnet-beta.solana.com')
            self.client = Client(rpc_url)
            
            # Load private key
            private_key_str = os.getenv('SOLANA_PRIVATE_KEY')
            if not private_key_str:
                raise ValueError("SOLANA_PRIVATE_KEY not found in environment variables")
            
            # Create keypair from private key
            private_key_bytes = base58.b58decode(private_key_str)
            self.keypair = Keypair.from_secret_key(private_key_bytes)
            self.public_key = self.keypair.public_key
            
            print(f"✅ Wallet initialized: {str(self.public_key)[:8]}...{str(self.public_key)[-8:]}")
            
        except Exception as e:
            print(f"❌ Wallet initialization failed: {e}")
            print("Make sure to:")
            print("1. Copy .env.example to .env")
            print("2. Add your wallet private key to .env")
            print("3. Never commit .env to version control!")
            raise
    
    def get_balance(self) -> float:
        """Get SOL balance"""
        try:
            response = self.client.get_balance(self.public_key)
            return response['result']['value'] / 1e9  # Convert lamports to SOL
        except Exception as e:
            print(f"Error getting balance: {e}")
            return 0.0
    
    def get_token_balance(self, mint_address: str) -> float:
        """Get specific token balance"""
        try:
            mint_pubkey = PublicKey(mint_address)
            response = self.client.get_token_accounts_by_owner(
                self.public_key,
                {"mint": mint_pubkey}
            )
            
            if response['result']['value']:
                account_data = response['result']['value'][0]['account']['data']
                # Parse token account data to get balance
                # This is simplified - you might need more robust parsing
                return 0.0  # Placeholder
            return 0.0
        except Exception as e:
            print(f"Error getting token balance: {e}")
            return 0.0
    
    def is_ready(self) -> bool:
        """Check if wallet is ready for trading"""
        return (self.client is not None and 
                self.keypair is not None and 
                self.public_key is not None)

# Global wallet instance
wallet_manager = SecureWalletManager()