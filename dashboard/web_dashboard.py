# dashboard/web_dashboard.py

from flask import Flask, render_template
import os
from config import trade_config as cfg

app = Flask(__name__)
LOG_PATH = cfg.LOG_FILE

@app.route("/")
def index():
    # Read log file
    logs = []
    if os.path.exists(LOG_PATH):
        with open(LOG_PATH, "r") as f:
            logs = f.readlines()
    return render_template("index.html", logs=logs, dry_run=cfg.DRY_RUN_MODE)

if __name__ == "__main__":
    app.run(debug=True, port=5000)