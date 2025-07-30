from flask import Flask, render_template_string, request, redirect
from multi_signal import scan_all_tokens
from safe_manager import SafeWalletManager
from strategy_selector import select_best_signal
from token_config import get_mint
from trade_executor import TradeExecutor
from jupiter_feed import fetch_latest_price_snapshot
import json

app = Flask(__name__)

TEMPLATE = """
<!DOCTYPE html>
<html>
<head><title>Signal Dashboard</title></head>
<body>
    <h2>📊 Signal Dashboard</h2>

    {% if success == "1" %}
    <p style="color:green;">✅ Trade confirmed and executed!</p>
    {% elif success == "0" %}
    <p style="color:red;">❌ Trade not confirmed.</p>
    {% endif %}

    <form method="POST" action="/set_mode">
        <label for="mode">Mode:</label>
        <select name="mode">
            {% for m in modes %}
            <option value="{{ m }}" {% if m == current_mode %}selected{% endif %}>{{ m }}</option>
            {% endfor %}
        </select>
        <button type="submit">Set Mode</button>
    </form>

    <h3>📈 Live Signals</h3>
    <table border="1">
        <tr><th>Token Pair</th><th>Signal</th></tr>
        {% for pair, signal in signals.items() %}
        <tr><td>{{ pair }}</td><td>{{ signal }}</td></tr>
        {% endfor %}
    </table>

    <h3>🎯 Next Trade Preview</h3>
    <p>Token: {{ preview.token }} | Signal: {{ preview.signal }} | Mint: {{ preview.mint }}</p>
    <form method="POST" action="/confirm_trade">
        <input type="hidden" name="token" value="{{ preview.token }}">
        <input type="hidden" name="signal" value="{{ preview.signal }}">
        <input type="hidden" name="mint" value="{{ preview.mint }}">
        <button type="submit">✅ Confirm Trade</button>
    </form>

    <h3>🧾 Recent Audit Log</h3>
    <table border="1">
        <tr><th>Time</th><th>Token</th><th>Signal</th><th>Price</th></tr>
        {% for entry in audit_log %}
        <tr>
            <td>{{ entry.timestamp }}</td>
            <td>{{ entry.token }}</td>
            <td>{{ entry.signal }}</td>
            <td>{{ entry.price.close }}</td>
        </tr>
        {% endfor %}
    </table>
</body>
</html>
"""

@app.route("/", methods=["GET"])
def dashboard():
    signals = scan_all_tokens()
    audit_log = load_audit_log(limit=10)
    best_pair = select_best_signal(signals)
    token = best_pair.split("/")[0] if best_pair else "SOL"
    signal = signals.get(best_pair, "sideways")
    mint = get_mint(token)
    success = request.args.get("success")

    return render_template_string(TEMPLATE,
                                  signals=signals,
                                  audit_log=audit_log,
                                  current_mode=SafeWalletManager.mode,
                                  modes=["manual", "auto_safe", "auto_all", "dry_run"],
                                  preview={"token": token, "signal": signal, "mint": mint},
                                  success=success)

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
    pair = f"{token}/USDC"

    price_snapshot = fetch_latest_price_snapshot(pair)

    confirmed = SafeWalletManager.confirm_trade(
        token=token,
        signal=signal,
        mint=mint,
        price_snapshot=price_snapshot
    )

    if confirmed:
        TradeExecutor.execute_trade(token, mint, signal)
        return redirect("/?success=1")
    return redirect("/?success=0")

def load_audit_log(limit=10):
    try:
        with open("audit_log.json", "r") as f:
            lines = f.readlines()[-limit:]
            return [json.loads(line) for line in lines]
    except:
        return []

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
