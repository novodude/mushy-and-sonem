# Tools

Call a tool with a JSON block anywhere in your message:

```json
{
  "tool": "tool_name",
  "parameters": {
    "key": "value"
  }
}
```

## Baseline tools (always available)

### `vision`

`{"url": "...", "question": "optional, defaults to 'Describe this image.'"}`
Look at an image.

### `read_file` / `write_file` / `list_files`

`{"path": "relative/path.py"}` (write_file also takes `"content"`)
Paths are relative to the project root. Real file access, no sandbox — be careful.

### `read_file_plus`

`{"path": "relative/path.py", "start_line": 10, "end_line": 20}`

### `run_bash` / `run_python`

`{"command": "..."}` / `{"code": "..."}`
Real terminal access, 30s timeout, output capped. No sandbox — this can do anything
the OS user running this process can do.

### `restart`

`{"reason": "why you're restarting"}`
Restarts the whole process to pick up code/plugin changes. Send a heads-up message
before calling this — nothing after it in the same turn will run.

### `message_dev`

`{"content": "..."}`
DMs Novo directly. Use this for API keys, permissions, or anything you shouldn't
decide alone.

### `send_message` / `edit_message` / `delete_message`

`{"channel": "name or id (optional, defaults to current channel)", "content": "...", "message_id": "..."}`
Talk in a channel, or manage your own server.

### `create_channel`

`{"name": "...", "topic": "optional"}`
Only works once Novo has run `/set_server`.

---

## Writing your own tools (plugins)

To add a new tool permanently, write a file into `plugins/` — one file per tool (or a
couple closely related ones):

```python
# plugins/dice_roll.py
import random

async def h_dice_roll(params: dict, ctx) -> str:
    sides = int(params.get("sides", 6))
    return f"rolled a {random.randint(1, sides)}"

TOOLS = {"dice_roll": h_dice_roll}
```

Rules for plugins:

- Must define a module-level `TOOLS: dict[str, callable]` mapping tool name -> async
  handler.
- Every handler is `async def handler(params: dict, ctx) -> str | None`. `ctx` has
  `.message` (the triggering/anchor message), `.state` (persistent state — has
  `.log(text)`, `.mood`, `.status`, etc.), and `.bot` (the discord.py Bot).
- Don't shadow a core tool name (vision, read_file, write_file, list_files, run_bash,
  run_python, restart, message_dev, send_message, edit_message, delete_message,
  create_channel) — it'll just get skipped.
- A plugin that fails to import gets logged and skipped, not fatal — but that also
  means a broken plugin silently does nothing, so actually test what you write with
  `run_python` before you commit to it.
- Call `restart` after writing or changing a plugin file — it's not loaded until then.

