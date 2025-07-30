# Imports
from flask import Flask, render_template_string, request, redirect
from multi_signal import scan_all_tokens
from safe_manager import SafeWalletManager
from strategy_selector import select_best_signal
from token_config import get_mint
from trade_executor import TradeExecutor
import json

app = Flask(__name__)

# HTML TEMPLATE (TEMPLATE = """ ... """)

# === ROUTES ===

@app.route("/", methods=["GET"])
def dashboard():
    signals = scan_all_tokens()
    audit_log = load_audit_log(limit=10)
    best_pair = select_best_signal(signals)
    token = best_pair.split("/")[0] if best_pair else "SOL"
    signal = signals.get(best_pair, "sideways")
    mint = get_mint(token)

    return render_template_string(TEMPLATE,
                                  signals=signals,
                                  audit_log=audit_log,
                                  current_mode=SafeWalletManager.mode,
                                  modes=["manual", "auto_safe", "auto_all", "dry_run"],
                                  preview={"token": token, "signal": signal, "mint": mint})

@app.route("/set_mode", methods=["POST"])
def set_mode():
    mode = request.form.get("mode")
    SafeWalletManager.mode = mode
    return redirect("/")

@app.route("/confirm_trade", methods=["POST"])
def confirm_trade():
    token = request.form.get("token")
    signal = request.form.get("signal")
    mint = request.form.get("mint")

    # Simulate price snapshot (can be replaced with real Jupiter fetch)
    price_snapshot = {"close": "N/A"}

    confirmed = SafeWalletManager.confirm_trade(
        token=token,
        signal=signal,
        mint=mint,
        price_snapshot=price_snapshot
    )

    if confirmed:
        TradeExecutor.execute_trade(token, mint, signal)
    return redirect("/")

# === UTILS ===

def load_audit_log(limit=10):
    try:
        with open("audit_log.json", "r") as f:
            lines = f.readlines()[-limit:]
            return [json.loads(line) for line in lines]
    except:
        return []

# === RUN SERVER ===

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
