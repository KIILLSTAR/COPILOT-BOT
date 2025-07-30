import json
from tabulate import tabulate

def load_audit_log(file_path="audit_log.json", limit=20):
    try:
        with open(file_path, "r") as f:
            lines = f.readlines()[-limit:]
            return [json.loads(line) for line in lines]
    except FileNotFoundError:
        print("❌ No audit log found.")
        return []

def format_log_entries(entries):
    table = []
    for entry in entries:
        table.append([
            entry.get("timestamp", "N/A"),
            entry.get("token", "N/A"),
            entry.get("signal", "N/A"),
            entry.get("price", {}).get("close", "N/A"),
            entry.get("mode", "N/A")
        ])
    return table

if __name__ == "__main__":
    entries = load_audit_log()
    if entries:
        headers = ["Time", "Token", "Signal", "Close Price", "Mode"]
        print(tabulate(format_log_entries(entries), headers=headers, tablefmt="pretty"))
    else:
        print("📭 No entries to display.")
