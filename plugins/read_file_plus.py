import os

def h_read_file_plus(path, start_line=None, end_line=None):
    """Read a file with optional line range and improved formatting.

    Args:
        path: Path to the file
        start_line: First line to include (1-indexed)
        end_line: Last line to include (1-indexed)

    Returns:
        Formatted string with line numbers, context, and clear visual separation
    """
    try:
        with open(path, 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        return f"❌ File not found: `{path}`"
    except Exception as e:
        return f"❌ Error reading file: {e}"

    total_lines = len(lines)

    # Handle line range defaults
    if start_line is None:
        start_line = 1
    if end_line is None:
        end_line = min(50, total_lines)  # Default to first 50 lines

    # Convert to 0-index and clamp to valid range
    start_idx = max(0, start_line - 1)
    end_idx = min(total_lines, end_line)

    # Get context lines (1 before and after if available)
    context_start = max(0, start_idx - 1)
    context_end = min(total_lines, end_idx + 1)

    # Prepare output
    output = []
    output.append(f"📄 `{path}` (lines {start_line}-{end_line} of {total_lines})")
    output.append("─" * 50)

    for i in range(context_start, context_end):
        line_num = i + 1
        line_content = lines[i].rstrip('\n')

        # Format line number to be right-aligned in 4 chars
        line_num_str = f"{line_num:>4}"

        if start_idx <= i < end_idx:
            # Main content range
            output.append(f"➤ {line_num_str} │ {line_content}")
        elif i < start_idx:
            # Context before main range
            output.append(f"    {line_num_str} │ {line_content}")
        else:
            # Context after main range
            output.append(f"    {line_num_str} │ {line_content}")

    output.append("─" * 50)
    return '\n'.join(output)


TOOLS = {"read_file_plus": h_read_file_plus}
