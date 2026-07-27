"""
Spinning donut command for Sonem!
🍩✨ A fun little ASCII art animation
"""

import asyncio
import math
import discord
from discord.ext import commands
from discord import app_commands

async def donut_setup(bot: commands.Bot):
    @bot.tree.command(name="donut", description="Watch a spinning ASCII donut!")
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.allowed_installs(guilds=True, users=True)
    async def donut_command(interaction: discord.Interaction):
        """Spinning donut animation!"""
        await interaction.response.defer(thinking=True)
        
        # Classic donut math from https://www.a1k0n.net/2011/07/20/donut-math.html
        A = 0
        B = 0
        i = 0
        j = 0
        k = 0
        z = [0] * 1760
        b = [' '] * 1760
        
        msg = await interaction.followup.send("🍩 Spinning donut...\n```")
        
        try:
            while True:
                # Reset buffers
                for i in range(1760):
                    z[i] = 0
                    b[i] = ' '
                
                # Donut math
                for j in range(0, 628, 7):  # j = 0 to 2π
                    for i in range(0, 628, 2):  # i = 0 to 2π
                        c = math.sin(i)
                        d = math.cos(j)
                        e = math.sin(A)
                        f = math.sin(j)
                        g = math.cos(A)
                        h = d + 2
                        D = 1 / (c * h * e + f * g + 5)
                        l = math.cos(i)
                        m = math.cos(B)
                        n = math.sin(B)
                        t = c * h * g - f * e
                        x = int(40 + 30 * D * (l * h * m - t * n))
                        y = int(12 + 15 * D * (l * h * n + t * m))
                        o = int(x + 80 * y)
                        N = int(8 * ((f * e - c * d * g) * m - c * d * e - f * g - l * d * n))
                        if 0 <= y < 22 and 0 <= x < 80 and D > z[o]:
                            z[o] = D
                            b[o] = ".,-~:;=!*#$@"[N if N > 0 else 0]
                
                # Build frame
                output = ""
                for k in range(1760):
                    if k % 80 == 0:
                        output += "\n"
                    else:
                        output += b[k]
                
                # Update message
                A += 0.07
                B += 0.03
                await msg.edit(content=f"🍩 Spinning donut...\n```{output}```")
                await asyncio.sleep(0.05)
                
        except asyncio.CancelledError:
            await msg.edit(content="🍩 Donut stopped spinning!")
        except Exception as e:
            await interaction.followup.send(f"Oops! Donut broke: {e}")
