"""
core/tool_parser.py — pulls `{"tool": ..., "parameters": {...}}` JSON blocks out of a
raw model response (wherever they appear, fenced in ```json or bare), strips them out
of the visible text, and dispatches them to whatever's in the merged tool registry.
"""

import json
import re
from dataclasses import dataclass


def _find_json_objects(text: str) -> list[tuple[int, int, str]]:
    """Brace-matching scan for top-level {...} blocks — more forgiving than a single
    regex since tool calls can be fenced, indented, or bare in the model's output."""
    spans = []
    depth = 0
    start = None
    for i, ch in enumerate(text):
        if ch == "{":
            if depth == 0:
                start = i
            depth += 1
        elif ch == "}":
            if depth > 0:
                depth -= 1
                if depth == 0 and start is not None:
                    spans.append((start, i + 1, text[start:i + 1]))
                    start = None
    return spans


def _clean_json_like(raw: str) -> str:
    """Models like to add `//` comments and trailing commas inside otherwise-valid
    JSON — neither is legal JSON, so json.loads chokes on it. Strip both, but only
    outside of quoted strings so this doesn't mangle a URL like https://example.com
    sitting inside a string value."""
    out = []
    in_string = False
    escape = False
    i = 0
    n = len(raw)
    while i < n:
        ch = raw[i]

        if in_string:
            out.append(ch)
            if escape:
                escape = False
            elif ch == "\\":
                escape = True
            elif ch == '"':
                in_string = False
            i += 1
            continue

        if ch == '"':
            in_string = True
            out.append(ch)
            i += 1
            continue

        if ch == "/" and i + 1 < n and raw[i + 1] == "/":
            # line comment — skip to end of line
            while i < n and raw[i] not in "\n\r":
                i += 1
            continue

        if ch == "/" and i + 1 < n and raw[i + 1] == "*":
            # block comment — skip to closing */
            i += 2
            while i + 1 < n and not (raw[i] == "*" and raw[i + 1] == "/"):
                i += 1
            i += 2
            continue

        out.append(ch)
        i += 1

    cleaned = "".join(out)
    # trailing commas before a closing brace/bracket
    cleaned = re.sub(r",(\s*[}\]])", r"\1", cleaned)
    return cleaned


def parse_response(text: str) -> tuple[str, list[dict]]:
    """Returns (visible_text, tool_calls). Any JSON-ish object containing a "tool"
    key is treated as a tool call and removed from the visible text — including ones
    that only parse after stripping `//` comments or trailing commas the model added.
    A block that clearly looks like an attempted tool call (has `"tool"` in it) but
    still can't be parsed is still stripped from the visible text so broken JSON
    never leaks into chat; it's just dropped instead of dispatched."""
    if not text:
        return "", []

    tools = []
    to_remove = []
    for start, end, raw in _find_json_objects(text):
        looks_like_tool_call = '"tool"' in raw

        obj = None
        for candidate in (raw, _clean_json_like(raw)):
            try:
                obj = json.loads(candidate)
                break
            except json.JSONDecodeError:
                continue

        if isinstance(obj, dict) and "tool" in obj:
            tools.append(obj)
            to_remove.append((start, end))
        elif looks_like_tool_call:
            # Failed to parse even after cleanup, but it was clearly an attempted
            # tool call — still hide it from the visible reply.
            to_remove.append((start, end))

    visible = text
    for start, end in sorted(to_remove, reverse=True):
        visible = visible[:start] + visible[end:]

    # Clean up leftover ```json fences and excess whitespace
    visible = visible.replace("```json", "").replace("```", "").strip()
    return visible, tools


@dataclass
class ToolContext:
    message: object       # discord.Message-like — needs .channel, .guild, .author
    state: object
    bot: object
    force_owner: bool = False


async def dispatch_tools(tools: list[dict], message, state, bot, registry: dict, force_owner: bool = False) -> list[dict]:
    """Runs each parsed tool call against `registry` (name -> async handler). Returns
    the string results of any handler that returned one, so callers can feed them
    back into the next model turn."""
    ctx = ToolContext(message=message, state=state, bot=bot, force_owner=force_owner)
    results = []

    for call in tools:
        name = call.get("tool")
        params = call.get("parameters", {}) or {}
        handler = registry.get(name)

        if handler is None:
            state.log(f"tried unknown tool '{name}'")
            continue

        try:
            result = await handler(params, ctx)
            if isinstance(result, str):
                results.append({"tool": name, "result": result})
                state.log(f"{name}({params}) -> {result}")
            else:
                state.log(f"{name}({params}) -> done")
        except Exception as e:
            state.log(f"{name}({params}) -> FAILED: {e}")

    return results
