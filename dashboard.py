from flask import Flask, render_template_string, request, redirect
from multi_signal import scan_all_tokens
from safe_manager import SafeWalletManager
import json

app = Flask(__name__)

TEMPLATE = """
<!DOCTYPE html>
<html>
<head><title>Signal Dashboard</title></head>
<body>
    <h2>📊 Signal Dashboard</h2>
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
    return render_template_string(TEMPLATE,
                                  signals=signals,
                                  audit_log=audit_log,
                                  current_mode=SafeWalletManager.mode,
                                  modes=["manual", "auto_safe", "auto_all", "dry_run"])

@app.route("/set_mode", methods=["POST"])
def set_mode():
    mode = request.form.get("mode")
    SafeWalletManager.mode = mode
    return redirect("/")

def load_audit_log(limit=10):
    try:
        with open("audit_log.json", "r") as f:
            lines = f.readlines()[-limit:]
            return [json.loads(line) for line in lines]
    except:
        return []

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
