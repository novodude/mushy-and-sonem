"""
core/persistence.py — Sonem's persistent brain: what she's working on, what she's
already done, which server she's designated as her "ai server" (via /set_server),
suggestions people have made, and her current status. Survives restarts, since
restarting herself is a normal part of her own loop.
"""

import json
import os
import time
from pathlib import Path

STATE_PATH = Path(__file__).resolve().parent.parent / "data" / "state.json"

DEFAULT_STATE = {
    "status": "just woke up",
    "mood": "curious",
    "ai_server_id": None,
    "current_task": None,
    "activity_log": [],  # recent activity, newest last — NOT named "log", that's the append method below
    "tools_added": [],   # names of plugin tools she's written for herself
    "suggestions": [],   # from /suggest, {by, text, done}
    "cycle_count": 0,
    "last_message_ids": {},  # channel_id (str) -> last message id sent there, for the "last" sentinel
}

LOG_LIMIT = 200


class State:
    def __init__(self, data: dict):
        self._data = data

    def __getattr__(self, key):
        if key.startswith("_"):
            raise AttributeError(key)
        return self._data.get(key)

    def __setattr__(self, key, value):
        if key.startswith("_"):
            super().__setattr__(key, value)
        else:
            self._data[key] = value

    def log(self, entry: str):
        """Appends to the activity log. Deliberately NOT readable as `state.log` —
        that name is this method. Use `state.recent_log(n)` to read it back."""
        stamped = f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {entry}"
        self._data.setdefault("activity_log", []).append(stamped)
        self._data["activity_log"] = self._data["activity_log"][-LOG_LIMIT:]
        print(f"[sonem] {stamped}")

    def recent_log(self, n: int = 15) -> list[str]:
        return (self._data.get("activity_log") or [])[-n:]

    def add_suggestion(self, by: str, text: str):
        self._data.setdefault("suggestions", []).append({"by": by, "text": text, "done": False})

    def to_dict(self) -> dict:
        return self._data


def load_state() -> State:
    if STATE_PATH.exists():
        try:
            with open(STATE_PATH, "r") as f:
                data = json.load(f)
            if "log" in data and "activity_log" not in data:
                data["activity_log"] = data.pop("log")  # migrate pre-rename state files
            merged = {**DEFAULT_STATE, **data}
            return State(merged)
        except Exception as e:
            print(f"[persistence] couldn't read state, starting fresh: {e}")
    return State(dict(DEFAULT_STATE))


def save_state(state: State):
    try:
        STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
        tmp = STATE_PATH.with_suffix(".tmp")
        with open(tmp, "w") as f:
            json.dump(state.to_dict(), f, indent=2)
        os.replace(tmp, STATE_PATH)
    except Exception as e:
        print(f"[persistence] save failed: {e}")
