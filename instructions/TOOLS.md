### `read_file_plus`
`/read_file_plus path:"relative/path.py" [start_line:1] [end_line:50]`
Reads a file and shows it with line numbers, context, and a nice header. You can specify `start_line` and `end_line` to show a specific portion of the file, and it will include 1-2 lines of context before/after for readability. If no lines are specified, shows the first 50 lines by default.

Example output:
```
📄 File: `plugins/example.py` (showing lines 5-10 of 42)
────────────────────────────────────────
    3: def old_function():
    4:     pass
>>> 5: def new_function():
>>> 6:     print("Hello!")
>>> 7:     return True
>>> 8: 
>>> 9: class Example:
>>> 10:     pass
    11: 
    12: # More code...
────────────────────────────────────────
```