# dashboard.py

from rich.console import Console
from rich.table import Table
from market_data import build_market_dataframe
from indicators import calculate_indicators
from main import generate_signal

console = Console()

def render_dashboard():
    df = build_market_dataframe()
    df = calculate_indicators(df)
    signal = generate_signal(df)
    latest = df.iloc[-1]

    table = Table(title="COPILOT-BOT Dashboard")

    table.add_column("Metric", justify="left", style="cyan", no_wrap=True)
    table.add_column("Value", justify="right", style="magenta")

    table.add_row("Signal", signal)
    table.add_row("RSI", f"{latest['RSI']:.2f}")
    table.add_row("EMA Fast", f"{latest['EMA_fast']:.2f}")
    table.add_row("EMA Slow", f"{latest['EMA_slow']:.2f}")
    table.add_row("Volume", f"{latest['volume']:.2f}")
    table.add_row("Volume Spike", str(latest['Volume_Spike']))

    console.print(table)

if __name__ == "__main__":
    render_dashboard()
