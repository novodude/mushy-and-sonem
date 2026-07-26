import discord
from discord import app_commands
from discord.ext import commands
import os

class ReadFilePlus(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="read_file_plus", description="Read a file with line numbers and context")
    @app_commands.describe(path="Path to the file", start_line="Starting line (optional)", end_line="Ending line (optional)")
    async def read_file_plus(self, interaction: discord.Interaction, path: str, start_line: int = None, end_line: int = None):
        try:
            # Check if file exists
            if not os.path.exists(path):
                await interaction.response.send_message(f"File not found: {path}", ephemeral=True)
                return

            # Read file content
            with open(path, 'r') as file:
                lines = file.readlines()

            total_lines = len(lines)

            # Handle line range
            if start_line is None:
                start_line = 1
            if end_line is None or end_line > total_lines:
                end_line = total_lines
            if start_line < 1:
                start_line = 1
            if end_line < start_line:
                end_line = start_line

            # Get context lines (2 before and after)
            context_start = max(1, start_line - 2)
            context_end = min(total_lines, end_line + 2)

            # Prepare output
            output = []
            output.append(f"📄 File: `{path}` (showing lines {start_line}-{end_line} of {total_lines})")
            output.append("────────────────────────────────────────")

            for i in range(context_start, context_end + 1):
                line = lines[i-1].rstrip('\n')
                if i >= start_line and i <= end_line:
                    output.append(f">>> {i:4d}: {line}")
                else:
                    output.append(f"    {i:4d}: {line}")

            output.append("────────────────────────────────────────")

            # Split into chunks if too long
            chunks = []
            current_chunk = ""
            for line in output:
                if len(current_chunk) + len(line) + 1 > 2000:
                    chunks.append(current_chunk)
                    current_chunk = ""
                current_chunk += line + "\n"
            if current_chunk:
                chunks.append(current_chunk)

            # Send response
            await interaction.response.send_message(chunks[0], ephemeral=True)
            for chunk in chunks[1:]:
                await interaction.followup.send(chunk, ephemeral=True)

        except Exception as e:
            await interaction.response.send_message(f"Error reading file: {str(e)}", ephemeral=True)

async def setup(bot):
    await bot.add_cog(ReadFilePlus(bot))
