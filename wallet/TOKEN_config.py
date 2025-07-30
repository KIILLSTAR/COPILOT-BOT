# wallet/TOKEN_config.py

# ✅ List of supported tokens for signal detection and trading
TOKEN_LIST = [
    "SOL",
    "USDC",
    "BONK",
    "JUP",
    "ETH",
    "BTC",
    "RAY",
    "SRM"
]

# ✅ Metadata for each token: mint address, decimals, display name
TOKEN_META = {
    "SOL": {
        "mint": "So11111111111111111111111111111111111111112",
        "decimals": 9,
        "name": "Solana"
    },
    "USDC": {
        "mint": "EPjFWdd5AufqSSqeM2qAqAqAqAqAqAqAqAqAqAqAqAqA",
        "decimals": 6,
        "name": "USD Coin"
    },
    "BONK": {
        "mint": "DezX3zY3Z3Z3Z3Z3Z3Z3Z3Z3Z3Z3Z3Z3Z3Z3Z3Z3Z3Z3",
        "decimals": 5,
        "name": "Bonk"
    },
    "JUP": {
        "mint": "JUPZ3Z3Z3Z3Z3Z3Z3Z3Z3Z3Z3Z3Z3Z3Z3Z3Z3Z3Z3Z3",
        "decimals": 6,
        "name": "Jupiter"
    },
    "ETH": {
        "mint": "2ndETHmintAddressHere",
        "decimals": 8,
        "name": "Ethereum (Wormhole)"
    },
    "BTC": {
        "mint": "BTCmintAddressHere",
        "decimals": 8,
        "name": "Bitcoin (Wormhole)"
    },
    "RAY": {
        "mint": "4k3Dyjzvzp8e2Y2X2X2X2X2X2X2X2X2X2X2X2X2X2X2",
        "decimals": 6,
        "name": "Raydium"
    },
    "SRM": {
        "mint": "SRMmintAddressHere",
        "decimals": 6,
        "name": "Serum"
    }
}

# ✅ Utility function (optional)
def get_token_mint(token_symbol: str) -> str:
    return TOKEN_META.get(token_symbol, {}).get("mint", "")

def get_token_decimals(token_symbol: str) -> int:
    return TOKEN_META.get(token_symbol, {}).get("decimals", 0)
