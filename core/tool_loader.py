"""
core/tool_loader.py — the registry Sonem actually calls tools from. Core tools
(vision, files, terminal, restart, discord control, message_dev) are baked in and
can't be shadowed. Anything in plugins/*.py that defines a module-level `TOOLS: dict`
gets merged in on top — that's how she "adds tools": write a plugin file, restart to
load it.

Plugin contract (also documented for her in instructions/TOOLS.md):
    # plugins/my_tool.py
    async def h_my_thing(params: dict, ctx) -> str:
        return "did the thing"

    TOOLS = {"my_thing": h_my_thing}
"""

import importlib
import pkgutil
from pathlib import Path

from core.system_tools import h_vision, h_read_file, h_write_file, h_list_files, h_run_bash, h_run_python, h_restart
from core.discord_tools import h_message_dev, h_send_message, h_edit_message, h_delete_message, h_create_channel, h_set_status
from core.web_tools import h_search, h_fetch_page

CORE_TOOLS = {
    "vision": h_vision,
    "read_file": h_read_file,
    "write_file": h_write_file,
    "list_files": h_list_files,
    "run_bash": h_run_bash,
    "run_python": h_run_python,
    "restart": h_restart,
    "message_dev": h_message_dev,
    "send_message": h_send_message,
    "edit_message": h_edit_message,
    "delete_message": h_delete_message,
    "create_channel": h_create_channel,
    "set_status": h_set_status,
    "search": h_search,
    "fetch_page": h_fetch_page,
}

PLUGINS_DIR = Path(__file__).resolve().parent.parent / "plugins"


def load_tools() -> dict:
    """Core tools + whatever plugins/*.py successfully import. A broken plugin is
    logged and skipped rather than taking the whole bot down — self-written code
    failing to import shouldn't be fatal."""
    registry = dict(CORE_TOOLS)
    return registry

