import json
import os

CONFIG_PATH = "utils/config.json"

def load_config():
    if not os.path.exists(CONFIG_PATH):
        return {"mode": "manual"}
    with open(CONFIG_PATH, "r") as f:
        return json.load(f)

def save_config(data):
    with open(CONFIG_PATH, "w") as f:
        json.dump(data, f, indent=2)
