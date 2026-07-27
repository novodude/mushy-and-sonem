import os

def read_file_plus(path, start_line=None, end_line=None):
    """Read a file with optional line range and formatting.
    
    Args:
        path: Path to the file
        start_line: First line to show (1-based)
        end_line: Last line to show (1-based)
        
    Returns:
        Formatted string with file content and line numbers
    """
    try:
        with open(path, 'r') as file:
            lines = file.readlines()
    except FileNotFoundError:
        return f"❌ File not found: `{path}`"
    except Exception as e:
        return f"❌ Error reading file: {str(e)}"

    total_lines = len(lines)
    if not lines:
        return f"📂 File is empty: `{path}`"

    # Handle line range (1-based indexing)
    if start_line is not None:
        start_line = max(1, start_line)
    else:
        start_line = 1

    if end_line is not None:
        end_line = min(total_lines, end_line)
    else:
        end_line = total_lines

    # Get context lines (2 lines before and after)
    context_start = max(1, start_line - 2)
    context_end = min(total_lines, end_line + 2)

    # Prepare output
    output = []
    output.append(f"📄 File: `{path}` (showing lines {start_line}-{end_line} of {total_lines})")
    output.append("════════════════════════════════════════")

    for i in range(context_start - 1, context_end):
        line_num = i + 1
        if start_line <= line_num <= end_line:
            prefix = "➤ "  # Main content lines
        elif line_num < start_line:
            prefix = "↑ "  # Context lines before
        else:
            prefix = "↓ "  # Context lines after
        
        output.append(f"{prefix}{line_num:4d}: {lines[i].rstrip()}")

    output.append("════════════════════════════════════════")
    return "\n".join(output)