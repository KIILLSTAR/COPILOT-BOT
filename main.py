"""
COPILOT BOT — Single Entry Point
Usage:
  python main.py          → runs the trading bot engine
  python main.py --web    → runs the web dashboard only
  python main.py --both   → runs both bot + dashboard (recommended)
"""
import sys, threading, os
sys.path.insert(0, os.path.dirname(__file__))

def run_bot():
    from core.bot_engine import run_bot as _run
    _run()

def run_dashboard():
    from dashboard.app import app
    port = int(os.environ.get("PORT", 5000))
    print(f"🌐 Dashboard running at http://localhost:{port}")
    app.run(host="0.0.0.0", port=port, debug=False, use_reloader=False)

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "--both"

    if mode == "--web":
        run_dashboard()
    elif mode == "--bot":
        run_bot()
    else:  # --both (default)
        dash_thread = threading.Thread(target=run_dashboard, daemon=True)
        dash_thread.start()
        run_bot()
