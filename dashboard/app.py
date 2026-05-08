"""
Web Dashboard — Flask app serving a real-time trading dashboard.
Mobile-optimized. Auto-refreshes every 10s. Dark theme.
"""
from flask import Flask, jsonify, render_template_string
import os, json
from core.simulation_engine import simulator
from core.price_fetcher import price_fetcher
from core.jupiter_perps import jupiter_perps
from config import trade_config as cfg

app = Flask(__name__)

DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>🤖 COPILOT BOT</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { background: #0a0a0f; color: #e0e0e0; font-family: 'Segoe UI', system-ui, sans-serif; font-size: 14px; }
  .header { background: linear-gradient(135deg, #1a1a2e, #16213e); padding: 16px 20px; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #2a2a4a; }
  .header h1 { font-size: 18px; color: #7c83fd; font-weight: 700; }
  .mode-badge { padding: 4px 10px; border-radius: 20px; font-size: 11px; font-weight: 700; letter-spacing: 1px; }
  .dry-run { background: #1a3a1a; color: #4caf50; border: 1px solid #4caf50; }
  .live { background: #3a1a1a; color: #f44336; border: 1px solid #f44336; }
  .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; padding: 16px; }
  .card { background: #12121f; border: 1px solid #2a2a4a; border-radius: 12px; padding: 16px; }
  .card.full { grid-column: 1 / -1; }
  .card-title { font-size: 11px; color: #7c83fd; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 10px; }
  .big-number { font-size: 26px; font-weight: 700; }
  .green { color: #4caf50; }
  .red { color: #f44336; }
  .neutral { color: #9e9e9e; }
  .sub { font-size: 11px; color: #666; margin-top: 4px; }
  .indicator-row { display: flex; justify-content: space-between; padding: 6px 0; border-bottom: 1px solid #1e1e2e; }
  .indicator-row:last-child { border-bottom: none; }
  .ind-label { color: #888; font-size: 12px; }
  .ind-value { font-weight: 600; font-size: 12px; }
  .position-card { background: #0e1a0e; border: 1px solid #2a4a2a; border-radius: 8px; padding: 12px; margin-bottom: 8px; }
  .position-card.short { background: #1a0e0e; border-color: #4a2a2a; }
  .pos-header { display: flex; justify-content: space-between; margin-bottom: 6px; }
  .trade-row { padding: 6px 0; border-bottom: 1px solid #1e1e2e; font-size: 12px; display: flex; justify-content: space-between; }
  .refresh-bar { text-align: center; padding: 8px; font-size: 11px; color: #444; }
  .signal-box { padding: 10px 14px; border-radius: 8px; margin-bottom: 8px; }
  .signal-long { background: #0d2010; border: 1px solid #2e7d32; }
  .signal-short { background: #200d0d; border: 1px solid #7d2e2e; }
  .signal-none { background: #1a1a1a; border: 1px solid #333; }
  .tag { display: inline-block; padding: 2px 8px; border-radius: 10px; font-size: 10px; font-weight: 700; }
  .tag-long { background: #1b5e20; color: #a5d6a7; }
  .tag-short { background: #b71c1c; color: #ef9a9a; }
  .tag-none { background: #333; color: #aaa; }
</style>
<script>
  let countdown = 30;
  function updateCountdown() {
    countdown--;
    document.getElementById('countdown').textContent = countdown + 's';
    if (countdown <= 0) { location.reload(); }
  }
  setInterval(updateCountdown, 1000);

  async function fetchData() {
    try {
      const r = await fetch('/api/data');
      const d = await r.json();
      updateDashboard(d);
    } catch(e) {}
  }

  function updateDashboard(d) {
    const p = d.portfolio;
    const m = d.market;
    const s = d.signal;

    // Balance
    document.getElementById('balance').textContent = '$' + p.balance.toLocaleString('en-US', {minimumFractionDigits: 2});
    const pnlEl = document.getElementById('total-pnl');
    pnlEl.textContent = (p.total_pnl >= 0 ? '+' : '') + '$' + p.total_pnl.toFixed(2);
    pnlEl.className = 'big-number ' + (p.total_pnl >= 0 ? 'green' : 'red');

    // Market
    document.getElementById('eth-price').textContent = '$' + (m.mark_price || p.eth_price).toLocaleString();
    document.getElementById('funding').textContent = (m.funding_rate_hourly * 100).toFixed(4) + '%';
    document.getElementById('oi-ratio').textContent = m.oi_ratio + 'x';
    document.getElementById('sentiment').textContent = m.market_sentiment || 'NEUTRAL';
    document.getElementById('volume').textContent = '$' + (m.volume_24h || 0).toLocaleString();

    // Signal
    const sigBox = document.getElementById('signal-box');
    const dir = s.direction;
    sigBox.className = 'signal-box signal-' + dir;
    document.getElementById('sig-dir').className = 'tag tag-' + dir;
    document.getElementById('sig-dir').textContent = dir.toUpperCase();
    document.getElementById('sig-conf').textContent = (s.confidence * 100).toFixed(1) + '%';
    document.getElementById('sig-reason').textContent = s.reason || '—';

    const ind = s.indicators || {};
    document.getElementById('ind-rsi').textContent = (ind.rsi || 0).toFixed(1);
    document.getElementById('ind-ema9').textContent = '$' + (ind.ema9 || 0).toFixed(0);
    document.getElementById('ind-ema21').textContent = '$' + (ind.ema21 || 0).toFixed(0);
    document.getElementById('ind-bb').textContent = (ind.bb_pct_b * 100 || 0).toFixed(1) + '%';

    // Stats
    document.getElementById('trades').textContent = p.total_trades;
    document.getElementById('winrate').textContent = p.win_rate + '%';
    document.getElementById('open-pos').textContent = p.open_positions;

    // Positions
    const posDiv = document.getElementById('positions');
    posDiv.innerHTML = '';
    if (p.positions && p.positions.length > 0) {
      p.positions.forEach(pos => {
        const pnlClass = pos.pnl >= 0 ? 'green' : 'red';
        posDiv.innerHTML += `
          <div class="position-card ${pos.side}">
            <div class="pos-header">
              <span class="tag tag-${pos.side}">${pos.side.toUpperCase()}</span>
              <span class="${pnlClass}" style="font-weight:700">${pos.pnl >= 0 ? '+' : ''}$${pos.pnl.toFixed(2)}</span>
            </div>
            <div style="display:flex;justify-content:space-between;font-size:12px;color:#888;">
              <span>Entry: $${pos.entry}</span><span>Size: $${pos.size_usd} @ ${pos.leverage}x</span>
            </div>
            <div style="display:flex;justify-content:space-between;font-size:11px;color:#555;margin-top:4px;">
              <span>SL: $${pos.sl}</span><span>TP: $${pos.tp}</span>
            </div>
          </div>`;
      });
    } else {
      posDiv.innerHTML = '<p style="color:#444;font-size:12px;text-align:center;padding:16px;">No open positions</p>';
    }

    // Recent trades
    const tradesDiv = document.getElementById('trades-list');
    tradesDiv.innerHTML = '';
    if (p.recent_trades && p.recent_trades.length > 0) {
      [...p.recent_trades].reverse().forEach(t => {
        const pnlClass = t.pnl >= 0 ? 'green' : 'red';
        tradesDiv.innerHTML += `
          <div class="trade-row">
            <span class="tag tag-${t.side}" style="margin-right:6px">${t.side.toUpperCase()}</span>
            <span style="color:#888">$${t.entry} → $${t.exit || '—'}</span>
            <span class="${pnlClass}" style="font-weight:700">${t.pnl >= 0 ? '+' : ''}$${t.pnl.toFixed(2)}</span>
          </div>`;
      });
    } else {
      tradesDiv.innerHTML = '<p style="color:#444;font-size:12px;text-align:center;padding:12px;">No trades yet</p>';
    }
  }

  setInterval(fetchData, 10000);
  window.onload = fetchData;
</script>
</head>
<body>

<div class="header">
  <h1>🤖 COPILOT BOT</h1>
  <span class="mode-badge {{ 'dry-run' if dry_run else 'live' }}">
    {{ '🧪 DRY RUN' if dry_run else '🔴 LIVE' }}
  </span>
</div>

<div class="grid">

  <!-- Balance -->
  <div class="card">
    <div class="card-title">Balance</div>
    <div class="big-number green" id="balance">Loading…</div>
    <div class="sub">Simulated starting: $10,000</div>
  </div>

  <!-- Total PnL -->
  <div class="card">
    <div class="card-title">Total PnL</div>
    <div class="big-number" id="total-pnl">—</div>
    <div class="sub" id="trades">— trades</div>
  </div>

  <!-- Signal -->
  <div class="card full">
    <div class="card-title">Latest Signal</div>
    <div class="signal-box signal-none" id="signal-box">
      <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;">
        <span class="tag tag-none" id="sig-dir">—</span>
        <span style="font-weight:700;font-size:16px" id="sig-conf">—</span>
      </div>
      <div style="font-size:11px;color:#888" id="sig-reason">Waiting for data…</div>
    </div>
    <div class="card-title" style="margin-top:12px">Indicators</div>
    <div class="indicator-row"><span class="ind-label">RSI (14)</span><span class="ind-value" id="ind-rsi">—</span></div>
    <div class="indicator-row"><span class="ind-label">EMA 9</span><span class="ind-value" id="ind-ema9">—</span></div>
    <div class="indicator-row"><span class="ind-label">EMA 21</span><span class="ind-value" id="ind-ema21">—</span></div>
    <div class="indicator-row"><span class="ind-label">Bollinger %B</span><span class="ind-value" id="ind-bb">—</span></div>
  </div>

  <!-- Market Data -->
  <div class="card full">
    <div class="card-title">Jupiter ETH-PERP Market</div>
    <div class="indicator-row"><span class="ind-label">Mark Price</span><span class="ind-value" id="eth-price">—</span></div>
    <div class="indicator-row"><span class="ind-label">Funding Rate (1h)</span><span class="ind-value" id="funding">—</span></div>
    <div class="indicator-row"><span class="ind-label">OI Ratio (L/S)</span><span class="ind-value" id="oi-ratio">—</span></div>
    <div class="indicator-row"><span class="ind-label">Market Sentiment</span><span class="ind-value" id="sentiment">—</span></div>
    <div class="indicator-row"><span class="ind-label">24h Volume</span><span class="ind-value" id="volume">—</span></div>
  </div>

  <!-- Stats -->
  <div class="card">
    <div class="card-title">Performance</div>
    <div class="indicator-row"><span class="ind-label">Win Rate</span><span class="ind-value green" id="winrate">—</span></div>
    <div class="indicator-row"><span class="ind-label">Open Positions</span><span class="ind-value" id="open-pos">—</span></div>
  </div>

  <!-- Open Positions -->
  <div class="card">
    <div class="card-title">Open Positions</div>
    <div id="positions"><p style="color:#444;font-size:12px;text-align:center;padding:16px">Loading…</p></div>
  </div>

  <!-- Trade History -->
  <div class="card full">
    <div class="card-title">Recent Trades</div>
    <div id="trades-list"><p style="color:#444;font-size:12px;text-align:center;padding:12px">Loading…</p></div>
  </div>

</div>

<div class="refresh-bar">Auto-refresh in <span id="countdown">30</span>s · Jupiter ETH-PERP · {{ 'DRY RUN MODE' if dry_run else 'LIVE MODE' }}</div>

</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(DASHBOARD_HTML, dry_run=cfg.DRY_RUN)

@app.route("/api/data")
def api_data():
    portfolio = simulator.get_portfolio_summary()
    market = jupiter_perps.get_market_summary()
    from strategy.signal_detector import detect_signal
    signal = detect_signal(cfg)
    return jsonify({
        "portfolio": portfolio,
        "market": market,
        "signal": signal,
        "mode": "dry_run" if cfg.DRY_RUN else "live"
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
