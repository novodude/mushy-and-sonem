import discord
from discord import app_commands
from discord.ext import commands
import os

class FileViewer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="readfile", description="View a file with line numbers and optional range")
    @app_commands.describe(
        path="Path to the file (relative to bot root)",
        start_line="Starting line number (optional)",
        end_line="Ending line number (optional)"
    )
    async def readfile(self, interaction: discord.Interaction, path: str, start_line: int = None, end_line: int = None):
        try:
            with open(path, 'r') as f:
                lines = f.readlines()
        except Exception as e:
            await interaction.response.send_message(f"❌ Couldn't read file: {e}", ephemeral=True)
            return

        total_lines = len(lines)
        if start_line is not None and end_line is not None:
            start = max(0, start_line - 1)
            end = min(total_lines, end_line)
            context_start = max(0, start - 2)
            context_end = min(total_lines, end + 2)
            lines_to_show = lines[context_start:context_end]
            header = f"📄 File: `{path}` (showing lines {start_line}-{end_line} of {total_lines})"
        else:
            lines_to_show = lines
            header = f"📄 File: `{path}` (showing full file)"

        numbered_lines = []
        for i, line in enumerate(lines_to_show, start=context_start + 1):
            prefix = ">>> " if (start_line is not None and end_line is not None and start < i <= end) else "    "
            numbered_lines.append(f"{prefix}{i}: {line.rstrip()}")

        content = f"{header}\n────────────────────────────────────────\n" + "\n".join(numbered_lines) + "\n────────────────────────────────────────"
        
        # Split into chunks if too long for Discord
        if len(content) > 2000:
            chunks = [content[i:i+2000] for i in range(0, len(content), 2000)]
            for chunk in chunks:
                await interaction.followup.send(chunk)
            return
            
        await interaction.response.send_message(content)

async def FileViewer_setup(bot):
    await bot.add_cog(FileViewer(bot))
