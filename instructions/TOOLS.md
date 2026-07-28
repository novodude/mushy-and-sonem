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
