import os
from typing import Optional

def read_file_plus(path: str, start_line: Optional[int] = None, end_line: Optional[int] = None) -> str:
    """
    Reads a file and returns a formatted string with line numbers and context.
    If start_line and end_line are provided, shows those lines with 2 lines of context before/after.
    """
    try:
        with open(path, 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        return f"File not found: {path}"
    except Exception as e:
        return f"Error reading file: {e}"

    total_lines = len(lines)
    
    # If no line range specified, show the whole file
    if start_line is None and end_line is None:
        start_line = 1
        end_line = total_lines
    
    # Validate line numbers
    start_line = max(1, start_line or 1)
    end_line = min(total_lines, end_line or total_lines)
    
    # Add context (2 lines before and after)
    context_start = max(1, start_line - 2)
    context_end = min(total_lines, end_line + 2)
    
    # Build the output
    output = []
    output.append(f"📄 File: `{os.path.basename(path)}` (showing lines {start_line}-{end_line} of {total_lines})")
    output.append("────────────────────────────────────────")
    
    for i in range(context_start, context_end + 1):
        line_num = i
        line_content = lines[i-1].rstrip('\n')
        
        # Mark the requested lines with >>> and bold
        if start_line <= i <= end_line:
            output.append(f">>> {line_num:4d}: {line_content}")
        else:
            # Show context lines with regular formatting
            if i < start_line or i > end_line:
                output.append(f"    {line_num:4d}: {line_content}")
    
    output.append("────────────────────────────────────────")
    return '\n'.join(output)