# token_config.py

TOKENS = {
    "ETH_PORTAL": {
        "mint": "7vfCXTqPU4fLrYjGzjY3VZz3yU2YfXz5pWjWkzXzjWkz",
        "role": "primary_collateral"
    },
    "SOL": {
        "mint": "So11111111111111111111111111111111111111112",
        "role": "secondary_collateral"
    },
    "USDC": {
        "mint": "EPjFWdd5AufqSSqeM2qAqAqAqAqAqAqAqAqAqAqAqAqAqAqAq",
        "role": "volatility_hedge"
    }
}

def get_mint(token_name: str) -> str:
    return TOKENS[token_name]["mint"]
