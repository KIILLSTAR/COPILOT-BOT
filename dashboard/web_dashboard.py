# web_dashboard.py

from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static
from market_data import build_market_dataframe
from indicators import calculate_indicators
from main import generate_signal

class BotDashboard(App):
    CSS_PATH = "dashboard.css"

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        yield Static(self.render_metrics())

    def render_metrics(self) -> str:
        df = build_market_dataframe()
        df = calculate_indicators(df)
        signal = generate_signal(df)
        latest = df.iloc[-1]

        return (
            f"\n[ COPILOT-BOT Web Dashboard ]\n\n"
            f"Signal: {signal}\n"
            f"RSI: {latest['RSI']:.2f}\n"
            f"EMA Fast: {latest['EMA_fast']:.2f}\n"
            f"EMA Slow: {latest['EMA_slow']:.2f}\n"
            f"Volume: {latest['volume']:.2f}\n"
            f"Volume Spike: {latest['Volume_Spike']}\n"
        )

if __name__ == "__main__":
    BotDashboard().run()
