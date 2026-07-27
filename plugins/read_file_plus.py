import os
from typing import Optional

def read_file_plus(path: str, start_line: Optional[int] = None, end_line: Optional[int] = None) -> str:
    """
    Reads a file and returns a nicely formatted string with:
    - Line numbers
    - Context lines before/after requested range
    - Clear visual indicators for the requested range
    - Graceful handling of edge cases
    
    Args:
        path: Relative path to the file
        start_line: First line to show (1-based, inclusive)
        end_line: Last line to show (1-based, inclusive)
        
    Returns:
        Formatted string with file contents
    """
    try:
        with open(path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except FileNotFoundError:
        return f"❌ File not found: `{path}`"
    except Exception as e:
        return f"❌ Error reading file: {str(e)}"
    
    if not lines:
        return f"📄 File: `{path}` (empty)"
    
    total_lines = len(lines)
    
    # Handle default values and edge cases
    if start_line is None:
        start_line = 1
    if end_line is None:
        end_line = total_lines
    
    # Convert to 0-based indices and clamp to valid range
    start_idx = max(0, min(start_line - 1, total_lines - 1))
    end_idx = max(0, min(end_line - 1, total_lines - 1))
    
    # Include 2 lines of context before/after if possible
    context_start = max(0, start_idx - 2)
    context_end = min(total_lines - 1, end_idx + 2)
    
    # Build the output
    header = f"📄 File: `{path}` (showing lines {start_line}-{end_line} of {total_lines})"
    separator = "────────────────────────────────────────"
    
    output = [header, separator]
    
    for i in range(context_start, context_end + 1):
        line_num = i + 1
        line_content = lines[i].rstrip()
        
        # Mark the requested range with >>>
        if start_idx <= i <= end_idx:
            output.append(f">>> {line_num:4d}: {line_content}")
        else:
            output.append(f"    {line_num:4d}: {line_content}")
    
    output.append(separator)
    return '\n'.join(output)