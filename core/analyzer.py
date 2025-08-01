# analyzer.py

from collections import defaultdict
from datetime import datetime

def parse_logs(log_entries):
    """
    Parses structured log entries into a usable format.
    Assumes each entry is a dict with keys: timestamp, asset, signal_type, conviction_level
    """
    parsed = []
    for entry in log_entries:
        parsed.append({
            "time": datetime.fromisoformat(entry["timestamp"]),
            "asset": entry["asset"],
            "signal": entry["signal_type"],
            "conviction": entry.get("conviction_level", None)
        })
    return parsed

def signal_stats(parsed_logs):
    """
    Returns frequency of each signal type per asset.
    """
    stats = defaultdict(lambda: defaultdict(int))
    for entry in parsed_logs:
        stats[entry["asset"]][entry["signal"]] += 1
    return stats

def detect_flip_flops(parsed_logs, cooldown_threshold=3):
    """
    Flags assets that were switched too frequently.
    """
    flip_flops = []
    last_asset = None
    last_time = None

    for entry in parsed_logs:
        if last_asset and entry["asset"] != last_asset:
            time_diff = (entry["time"] - last_time).seconds
            if time_diff < cooldown_threshold:
                flip_flops.append({
                    "from": last_asset,
                    "to": entry["asset"],
                    "time": entry["time"],
                    "seconds_between": time_diff
                })
        last_asset = entry["asset"]
        last_time = entry["time"]
    return flip_flops

def conviction_trace(parsed_logs):
    """
    Tracks how long each conviction level lasted before switching.
    """
    traces = []
    current = None
    start_time = None

    for entry in parsed_logs:
        if current != entry["conviction"]:
            if current is not None:
                duration = (entry["time"] - start_time).seconds
                traces.append({
                    "conviction": current,
                    "duration_seconds": duration
                })
            current = entry["conviction"]
            start_time = entry["time"]
    return traces