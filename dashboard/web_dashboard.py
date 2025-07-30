from flask import Flask, render_template, request, redirect
from dashboard.log_viewer import get_recent_logs
from wallet.TOKEN_config import TOKEN_LIST
from wallet.logger import log_info, log_event
# Optional: from wallet.trade_executer import execute_trade

app = Flask(__name__)

# ✅ Mode toggle state (simple in-memory for now)
current_mode = "AUTO"

def get_current_mode():
    return current_mode

def toggle_mode():
    global current_mode
    current_mode = "MANUAL" if current_mode == "AUTO" else "AUTO"
    log_event("MODE_TOGGLED", {"new_mode": current_mode})

# ✅ Home page
@app.route("/")
def index():
    logs = get_recent_logs(50)
    mode = get_current_mode()
    return render_template("index.html", logs=logs, mode=mode, tokens=TOKEN_LIST)

# ✅ Log viewer
@app.route("/logs")
def show_logs():
    logs = get_recent_logs(100)
    return render_template("logs.html", logs=logs)

# ✅ Mode toggle
@app.route("/toggle_mode", methods=["POST"])
def toggle_mode_route():
    toggle_mode()
    return redirect("/")

# ✅ Manual trade trigger
@app.route("/manual_trade", methods=["POST"])
def manual_trade():
    token = request.form.get("token")
    amount = float(request.form.get("amount", 0))

    # Optional: execute the trade
    # execute_trade(token, amount)

    log_event("MANUAL_TRADE", {"token": token, "amount": amount})
    log_info(f"Manual trade triggered: {amount} {token}")
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
