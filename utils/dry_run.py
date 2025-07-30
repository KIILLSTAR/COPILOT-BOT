# utils/dry_run.py

import os

# ✅ Default mode (can be overridden by env var or config file)
DRY_RUN = True

def is_dry_run() -> bool:
    """
    Returns whether the bot is in dry-run mode.
    Can be toggled via environment variable or config file later.
    """
    return DRY_RUN

def set_dry_run(value: bool):
    """
    Allows toggling dry-run mode programmatically.
    """
    global DRY_RUN
    DRY_RUN = value

def toggle_dry_run():
    """
    Flips the current dry-run mode.
    """
    global DRY_RUN
    DRY_RUN = not DRY_RUN
    return DRY_RUN
