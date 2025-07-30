from flask import Flask, render_template, request, redirect
app = Flask(__name__)
from wallet.wallet import SafeWalletManager
from cli.view_audit_log import get_audit_logs
from utils.config import load_config, save_config
from dashboard.log_viewer import get_recent_logs

@app.route("/logs")

def show_logs():
    logs = get_recent_logs(100)
    return render_template("logs.html", logs=logs)

@app.route("/")
def index():
    logs = get_audit_logs()
    mode = load_config().get("mode", "manual")
    return render_template("index.html", logs=logs, mode=mode)

@app.route("/toggle_mode", methods=["POST"])
def toggle_mode():
    config = load_config()
    current = config.get("mode", "manual")
    new_mode = "auto" if current == "manual" else "manual"
    config["mode"] = new_mode
    save_config(config)
    return redirect("/")

@app.route("/manual_trade", methods=["POST"])
def manual_trade():
    token = request.form.get("token")
    amount = float(request.form.get("amount", 0))
    # Call SafeWalletManager or trade_executer here
    log_event("MANUAL_TRADE", {"token": token, "amount": amount})
    return redirect("/")

@app.route("/confirm_trade", methods=["POST"])
def confirm_trade():
    trade_data = request.form.to_dict()
    wallet = SafeWalletManager()
    wallet.confirm_trade(trade_data)
    return redirect("/")
