# wallet/trade_executer.py

from wallet.TOKEN_config import TOKEN_META
from wallet.logger import log_info, log_error, log_event
from utils.dry_run import is_dry_run

def execute_trade(token: str, amount: float) -> bool:
    try:
        # ✅ Validate token metadata
        meta = TOKEN_META.get(token)
        if not meta:
            raise ValueError(f"Token '{token}' not found in TOKEN_META")

        mint = meta.get("mint")
        decimals = meta.get("decimals")

        if not mint or decimals is None:
            raise ValueError(f"Missing mint or decimals for token '{token}'")

        # ✅ Dry-run mode
        if is_dry_run():
            log_info(f"[DRY RUN] Would execute trade: {amount} {token} (mint: {mint}, decimals: {decimals})")
            log_event("DRY_RUN_TRADE", {
                "token": token,
                "amount": amount,
                "mint": mint,
                "decimals": decimals
            })
            return True

        # ✅ Real trade logic placeholder
        # Replace this with actual swap or transfer logic
        log_info(f"Executing trade: {amount} {token} (mint: {mint}, decimals: {decimals})")
        log_event("TRADE_EXECUTED", {
            "token": token,
            "amount": amount,
            "mint": mint,
            "decimals": decimals
        })

        return True

    except Exception as e:
        log_error(f"Trade execution failed for {token}: {str(e)}")
        log_event("TRADE_FAILED", {
            "token": token,
            "amount": amount,
            "error": str(e)
        })
        return False
