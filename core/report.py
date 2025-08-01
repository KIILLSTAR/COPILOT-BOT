# report.py

from core.analyzer import parse_logs, signal_stats, detect_flip_flops, conviction_trace
from core.visualizer import plot_signal_frequency, plot_asset_timeline, plot_pnl_simulation

def generate_report(log_entries, show_charts=False, price_lookup=None):
    """
    Runs post-loop analysis on dry-run logs.
    
    Args:
        log_entries (list): List of structured log dicts.
        show_charts (bool): Whether to render charts.
        price_lookup (dict): Optional price data for PnL simulation.
    """
    print("\n📊 Generating Dry-Run Report...\n")

    parsed = parse_logs(log_entries)

    # Signal frequency
    stats = signal_stats(parsed)
    print("✅ Signal Frequency per Asset:")
    for asset, signals in stats.items():
        print(f"  {asset}:")
        for signal, count in signals.items():
            print(f"    {signal}: {count}")
    if show_charts:
        plot_signal_frequency(stats)

    # Flip-flop detection
    flips = detect_flip_flops(parsed)
    if flips:
        print("\n🚨 Flip-Flop Alerts:")
        for flip in flips:
            print(f"  Switched from {flip['from']} to {flip['to']} after {flip['seconds_between']}s at {flip['time']}")
    else:
        print("\n✅ No flip-flops detected.")

    # Conviction trace
    traces = conviction_trace(parsed)
    print("\n🧠 Conviction Durations:")
    for trace in traces:
        print(f"  {trace['conviction']} held for {trace['duration_seconds']}s")

    # Asset timeline chart
    if show_charts:
        plot_asset_timeline(parsed)

    # Optional PnL simulation
    if show_charts and price_lookup:
        print("\n📈 Simulating PnL...")
        plot_pnl_simulation(parsed, price_lookup)

    print("\n✅ Report Complete.\n")