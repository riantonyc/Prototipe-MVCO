# abstraksi baca/tulis file JSON

# storage.py
import json
import os
from typing import Any

def ensure_dirs():
    os.makedirs("data", exist_ok=True)
    os.makedirs("SaveJson", exist_ok=True)

def load_json(path: str, default: Any = None):
    ensure_dirs()
    if not os.path.exists(path):
        return default if default is not None else []
    with open(path, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except:
            return default if default is not None else []

def save_json(path: str, data: Any):
    ensure_dirs()
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

