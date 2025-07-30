# wallet/trade_executer.py

from wallet.TOKEN_config import TOKEN_META
from wallet.logger import log_info, log_error, log_event

def execute_trade(token: str, amount: float):
    try:
        mint = TOKEN_META.get(token, {}).get("mint")
        decimals = TOKEN_META.get(token, {}).get("decimals")

        if not mint or decimals is None:
            raise ValueError(f"Token metadata missing for {token}")

        # ✅ Simulate trade logic (replace with actual swap call)
        log_info(f"Executing trade: {amount} {token} (mint: {mint}, decimals: {decimals})")

        # ✅ Log structured event
        log_event("TRADE_EXECUTED", {
            "token": token,
            "amount": amount,
            "mint": mint,
            "decimals": decimals
        })

        return True

    except Exception as e:
        log_error(f"Trade execution failed for {token}: {str(e)}")
        return False
