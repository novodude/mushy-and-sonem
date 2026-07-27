from core import bot
import discord
from discord import app_commands
import os

@bot.tree.command(name="read_file_plus", description="Read a file with line numbers and context")
@app_commands.describe(path="Path to the file (relative to bot directory)", start_line="Starting line (optional)", end_line="Ending line (optional)")
async def read_file_plus(interaction: discord.Interaction, path: str, start_line: int = None, end_line: int = None):
    try:
        # Safety check - no absolute paths or parent directory traversal
        if os.path.isabs(path) or ".." in path:
            await interaction.response.send_message("Error: Only relative paths are allowed", ephemeral=True)
            return

        try:
            with open(path, 'r') as f:
                lines = f.readlines()
        except FileNotFoundError:
            await interaction.response.send_message(f"File not found: {path}", ephemeral=True)
            return
        except Exception as e:
            await interaction.response.send_message(f"Error reading file: {str(e)}", ephemeral=True)
            return

        total_lines = len(lines)
        if start_line is None:
            start_line = 1
        if end_line is None or end_line > total_lines:
            end_line = total_lines

        # Adjust for 0-based indexing and add context
        context_start = max(0, start_line - 3)  # Show 2 lines before
        context_end = min(total_lines, end_line + 2)  # Show 2 lines after

        # Build the output
        output = f"📄 File: `{path}` (showing lines {start_line}-{end_line} of {total_lines})\n"
        output += "────────────────────────────────────────\n"

        for i, line in enumerate(lines[context_start:context_end], start=context_start + 1):
            prefix = ">>> " if start_line <= i <= end_line else "    "
            output += f"{prefix}{i}: {line}"

        output += "────────────────────────────────────────\n"

        # Split into chunks if too long
        if len(output) > 2000:
            chunks = [output[i:i+2000] for i in range(0, len(output), 2000)]
            await interaction.response.send_message(chunks[0])
            for chunk in chunks[1:]:
                await interaction.followup.send(chunk)
        else:
            await interaction.response.send_message(output)

    except Exception as e:
        await interaction.response.send_message(f"Error: {str(e)}", ephemeral=True)