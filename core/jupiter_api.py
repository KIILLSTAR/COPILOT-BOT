"""
Jupiter API Integration for ETH Trading
Handles both spot trading and perpetuals (when available)
"""
import requests
import json
import time
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from wallet.TOKEN_config import TOKEN_META

@dataclass
class QuoteRequest:
    input_mint: str
    output_mint: str
    amount: int
    slippage_bps: int = 50
    swap_mode: str = "ExactIn"
    only_direct_routes: bool = False
    as_legacy_transaction: bool = False

@dataclass
class SwapResponse:
    input_mint: str
    in_amount: str
    output_mint: str
    out_amount: str
    other_amount_threshold: str
    swap_mode: str
    slippage_bps: int
    platform_fee: Optional[Dict]
    price_impact_pct: str
    route_plan: List[Dict]

class JupiterAPI:
    def __init__(self, base_url: str = "https://quote-api.jup.ag/v6"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        })
    
    def get_quote(self, request: QuoteRequest) -> Optional[Dict[str, Any]]:
        """Get a quote for token swap"""
        try:
            params = {
                'inputMint': request.input_mint,
                'outputMint': request.output_mint,
                'amount': request.amount,
                'slippageBps': request.slippage_bps,
                'swapMode': request.swap_mode,
                'onlyDirectRoutes': str(request.only_direct_routes).lower(),
                'asLegacyTransaction': str(request.as_legacy_transaction).lower()
            }
            
            response = self.session.get(f"{self.base_url}/quote", params=params)
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            print(f"[ERROR] Failed to get quote: {e}")
            return None
    
    def get_swap_transaction(self, quote: Dict[str, Any], user_public_key: str, 
                           prioritization_fee_lamports: str = "auto") -> Optional[Dict[str, Any]]:
        """Get swap transaction from quote"""
        try:
            payload = {
                "quoteResponse": quote,
                "userPublicKey": user_public_key,
                "prioritizationFeeLamports": prioritization_fee_lamports
            }
            
            response = self.session.post(f"{self.base_url}/swap", json=payload)
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            print(f"[ERROR] Failed to get swap transaction: {e}")
            return None
    
    def get_price(self, token_addresses: List[str]) -> Optional[Dict[str, Any]]:
        """Get current prices for tokens"""
        try:
            params = {'ids': ','.join(token_addresses)}
            response = self.session.get("https://price.jup.ag/v4/price", params=params)
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            print(f"[ERROR] Failed to get prices: {e}")
            return None

class ETHPerpTrader:
    """ETH Perpetuals Trading Handler"""
    
    def __init__(self, jupiter_api: JupiterAPI):
        self.jupiter_api = jupiter_api
        self.eth_mint = TOKEN_META["ETH"]["mint"]
        self.usdc_mint = TOKEN_META["USDC"]["mint"]
    
    def get_eth_price(self) -> Optional[float]:
        """Get current ETH price in USDC"""
        try:
            # Get quote for 1 ETH to USDC
            eth_decimals = TOKEN_META["ETH"]["decimals"]
            amount = 10 ** eth_decimals  # 1 ETH
            
            quote_request = QuoteRequest(
                input_mint=self.eth_mint,
                output_mint=self.usdc_mint,
                amount=amount
            )
            
            quote = self.jupiter_api.get_quote(quote_request)
            if quote and 'outAmount' in quote:
                usdc_decimals = TOKEN_META["USDC"]["decimals"]
                price = int(quote['outAmount']) / (10 ** usdc_decimals)
                return price
            
            return None
            
        except Exception as e:
            print(f"[ERROR] Failed to get ETH price: {e}")
            return None
    
    def create_buy_order(self, usdc_amount: float, user_public_key: str, 
                        slippage_bps: int = 100) -> Optional[Dict[str, Any]]:
        """Create ETH buy order with USDC"""
        try:
            usdc_decimals = TOKEN_META["USDC"]["decimals"]
            amount_in_base_units = int(usdc_amount * (10 ** usdc_decimals))
            
            quote_request = QuoteRequest(
                input_mint=self.usdc_mint,
                output_mint=self.eth_mint,
                amount=amount_in_base_units,
                slippage_bps=slippage_bps
            )
            
            quote = self.jupiter_api.get_quote(quote_request)
            if not quote:
                return None
            
            swap_transaction = self.jupiter_api.get_swap_transaction(quote, user_public_key)
            return {
                'quote': quote,
                'transaction': swap_transaction,
                'side': 'buy',
                'input_amount': usdc_amount,
                'expected_output': int(quote['outAmount']) / (10 ** TOKEN_META["ETH"]["decimals"])
            }
            
        except Exception as e:
            print(f"[ERROR] Failed to create buy order: {e}")
            return None
    
    def create_sell_order(self, eth_amount: float, user_public_key: str, 
                         slippage_bps: int = 100) -> Optional[Dict[str, Any]]:
        """Create ETH sell order for USDC"""
        try:
            eth_decimals = TOKEN_META["ETH"]["decimals"]
            amount_in_base_units = int(eth_amount * (10 ** eth_decimals))
            
            quote_request = QuoteRequest(
                input_mint=self.eth_mint,
                output_mint=self.usdc_mint,
                amount=amount_in_base_units,
                slippage_bps=slippage_bps
            )
            
            quote = self.jupiter_api.get_quote(quote_request)
            if not quote:
                return None
            
            swap_transaction = self.jupiter_api.get_swap_transaction(quote, user_public_key)
            return {
                'quote': quote,
                'transaction': swap_transaction,
                'side': 'sell',
                'input_amount': eth_amount,
                'expected_output': int(quote['outAmount']) / (10 ** TOKEN_META["USDC"]["decimals"])
            }
            
        except Exception as e:
            print(f"[ERROR] Failed to create sell order: {e}")
            return None

# Legacy functions for backward compatibility
def execute_swap(wallet_address, input_mint, output_mint, amount, live=False):
    """Legacy function - deprecated, use JupiterAPI class instead"""
    if not live:
        print("[DRY RUN] Swap skipped.")
        return
    
    jupiter_api = JupiterAPI()
    quote_request = QuoteRequest(
        input_mint=input_mint,
        output_mint=output_mint,
        amount=int(amount * 1e6)  # assuming USDC/ETH decimals
    )
    
    quote = jupiter_api.get_quote(quote_request)
    if quote:
        swap_transaction = jupiter_api.get_swap_transaction(quote, wallet_address)
        if swap_transaction:
            print("[LIVE TRADE] Swap transaction prepared.")
            return swap_transaction
        else:
            raise Exception("Failed to create swap transaction")
    else:
        raise Exception("Failed to get quote")
