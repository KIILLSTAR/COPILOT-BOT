"""
Consolidated Safe Wallet Manager
Combines all safe wallet functionality
"""
import time
from typing import Dict, Any, Optional

# =============================================================================
# SAFE SWAP (from safe_wallet_manager/safe_swap.py)
# =============================================================================

def safe_execute_swap(client, wallet_address: str, mint: str, execute_swap_fn):
    """Execute a safe swap with balance checks"""
    from config import MIN_BALANCE_THRESHOLD
    from logger import log_transfer
    
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

# =============================================================================
# SAFE WALLET MANAGER CLASS
# =============================================================================

class SafeWalletManager:
    """
    Consolidated safe wallet manager with all functionality
    """
    
    def __init__(self):
        self.mode = "manual"  # Default mode
        self.balance_threshold = 0.01
        self.log_path = "./logs/"
    
    def set_mode(self, mode: str):
        """Set wallet manager mode"""
        valid_modes = ["manual", "auto_safe", "auto_all", "dry_run"]
        if mode in valid_modes:
            self.mode = mode
            print(f"✅ Wallet mode set to: {mode}")
        else:
            print(f"❌ Invalid mode. Valid modes: {valid_modes}")
    
    def check_balance(self, client, wallet_address: str) -> float:
        """Check wallet balance safely"""
        try:
            balance = client.get_balance(wallet_address)['result']['value'] / 1e9
            return balance
        except Exception as e:
            print(f"❌ Failed to get balance: {e}")
            return 0.0
    
    def is_balance_sufficient(self, balance: float) -> bool:
        """Check if balance is sufficient for operations"""
        return balance >= self.balance_threshold
    
    def safe_transfer(self, client, from_address: str, to_address: str, amount: float) -> Optional[str]:
        """Execute a safe transfer with balance checks"""
        from logger import log_transfer
        
        try:
            # Check balance first
            balance = self.check_balance(client, from_address)
            
            if not self.is_balance_sufficient(balance):
                print(f"⚠️ Insufficient balance: {balance:.6f} SOL (min: {self.balance_threshold:.6f})")
                return None
            
            if amount > balance:
                print(f"⚠️ Transfer amount ({amount:.6f}) exceeds balance ({balance:.6f})")
                return None
            
            # Execute transfer (simulated for now)
            tx_id = f"tx_{int(time.time())}"
            print(f"✅ Transfer executed: {amount:.6f} SOL from {from_address[:8]}... to {to_address[:8]}...")
            print(f"Transaction ID: {tx_id}")
            
            # Log the transfer
            log_transfer(from_address, to_address, amount, tx_id)
            
            return tx_id
            
        except Exception as e:
            print(f"❌ Transfer failed: {e}")
            return None
    
    def safe_swap(self, client, wallet_address: str, mint: str, execute_swap_fn):
        """Execute a safe swap"""
        safe_execute_swap(client, wallet_address, mint, execute_swap_fn)
    
    def get_status(self) -> Dict[str, Any]:
        """Get wallet manager status"""
        return {
            "mode": self.mode,
            "balance_threshold": self.balance_threshold,
            "log_path": self.log_path
        }

# =============================================================================
# GLOBAL INSTANCE
# =============================================================================

safe_wallet_manager = SafeWalletManager()

# =============================================================================
# EXPORTS
# =============================================================================

__all__ = [
    'SafeWalletManager', 'safe_wallet_manager', 'safe_execute_swap'
]