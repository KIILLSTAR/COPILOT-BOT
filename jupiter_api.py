import requests

def execute_swap(wallet_address, input_mint, output_mint, amount, live=False):
    if not live:
        print("[DRY RUN] Swap skipped.")
        return

    url = "https://quote-api.jup.ag/v6/swap"
    payload = {
        "userPublicKey": wallet_address,
        "inputMint": input_mint,
        "outputMint": output_mint,
        "amount": int(amount * 1e6),  # assuming USDC/ETH decimals
        "slippageBps": 50,
        "swapMode": "ExactIn"
    }

    response = requests.post(url, json=payload)
    if response.status_code == 200:
        print("[LIVE TRADE] Swap executed successfully.")
    else:
        raise Exception(f"Swap failed: {response.text}")
