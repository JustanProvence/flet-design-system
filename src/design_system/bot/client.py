"""
Discord Bot integration for the Flet Design System.

Implements a stateful Discord bot providing remote queries, color chip generation,
system status checks, and showcase file delivery directly into Discord channels.
"""

import os
import io
import discord
from discord.ext import commands
import aiohttp
from PIL import Image, ImageDraw
from design_system.tokens.manager import tokens

# Load environment variables (dotenv is handled via flet or manually)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Setup bot intents
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

@bot.event
async def on_ready():
    """
    Triggered when the Discord client establishes a successful websocket connection.
    """
    print(f"Logged in as {bot.user.name} (ID: {bot.user.id})")
    print("------")
    # Set status presence
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching, 
            name="Flet Design System (type !help)"
        )
    )

@bot.command(name="help")
async def help_command(ctx):
    """
    Displays the standard help commands and usages.
    """
    embed = discord.Embed(
        title="🎨 Flet Design System Bot",
        description="Interact and inspect your design tokens and components remotely!",
        color=discord.Color.blue()
    )
    embed.add_field(
        name="`!status`",
        value="Checks if the local Flet web server is online at port 8550.",
        inline=False
    )
    embed.add_field(
        name="`!tokens`",
        value="Lists global spacing, border-radius, and typography metadata.",
        inline=False
    )
    embed.add_field(
        name="`!color <token_name>`",
        value="Resolves a color token and draws a visual color chip (e.g., `!color primary`).",
        inline=False
    )
    embed.add_field(
        name="`!screenshot <light/dark>`",
        value="Uploads the pre-rendered showcase graphics of the Flet interface.",
        inline=False
    )
    embed.set_footer(text="Flet Design System • v0.1.0")
    await ctx.send(embed=embed)

@bot.command(name="status")
async def status(ctx):
    """
    Checks the local health status of the Flet web server.
    """
    target_url = "http://127.0.0.1:8550/"
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(target_url, timeout=3) as r:
                if r.status == 200:
                    embed = discord.Embed(
                        title="🟢 Flet Server: ONLINE",
                        description=f"The Design System showcase is active at {target_url}",
                        color=discord.Color.green()
                    )
                    embed.add_field(name="HTTP Status", value="`200 OK`", inline=True)
                    embed.add_field(name="Server Header", value=f"`{r.headers.get('server', 'Uvicorn')}`", inline=True)
                else:
                    embed = discord.Embed(
                        title="🟡 Flet Server: WARNING",
                        description=f"The server is responding, but returned status code {r.status}.",
                        color=discord.Color.gold()
                    )
        except Exception:
            embed = discord.Embed(
                title="🔴 Flet Server: OFFLINE",
                description="Failed to connect to the local Flet server on port 8550.",
                color=discord.Color.red()
            )
            embed.add_field(name="Action Required", value="Run `poetry run python3 src/design_system/main.py` locally.", inline=False)
            
    embed.set_footer(text="Flet Design System • v0.1.0")
    await ctx.send(embed=embed)

@bot.command(name="tokens")
async def show_tokens(ctx):
    """
    Returns lists of typography scales, spacings, and radiuses from tokens.json.
    """
    embed = discord.Embed(
        title="📐 Design System Tokens",
        description="Current global scale rules configured in `tokens.json`:",
        color=discord.Color.blue()
    )
    
    # Spacing
    spacing_text = "\n".join([f"• **{k}**: `{v}px`" for k, v in tokens.global_tokens["spacing"].items()])
    embed.add_field(name="📐 Spacing Scale", value=spacing_text, inline=True)
    
    # Corner Radiuses
    radius_text = "\n".join([f"• **{k}**: `{v}px`" for k, v in tokens.global_tokens["radius"].items()])
    embed.add_field(name="🟢 Border Radius", value=radius_text, inline=True)
    
    # Typography Font Sizes
    font_text = "\n".join([f"• **{k}**: `{v}px`" for k, v in tokens.global_tokens["typography"]["font-size"].items()])
    embed.add_field(name="🔤 Typography Font Sizes", value=font_text, inline=False)
    
    embed.set_footer(text="Flet Design System • v0.1.0")
    await ctx.send(embed=embed)

@bot.command(name="color")
async def resolve_color(ctx, name: str = None):
    """
    Resolves a semantic or primitive color and returns a dynamic color chip attachment.
    """
    if name is None:
        await ctx.send("❌ Please specify a color name (e.g., `!color primary` or `!color blue-600`)")
        return
        
    # Resolve color hex values
    light_hex = tokens.get_color(name, dark=False)
    dark_hex = tokens.get_color(name, dark=True)
    
    # Generate Pillow color chip image
    chip_size = (150, 150)
    image = Image.new("RGB", (320, 150), "#F1F5F9")
    draw = ImageDraw.Draw(image)
    
    # Draw light mode box on the left, dark mode box on the right
    draw.rectangle([0, 0, 160, 150], fill=light_hex)
    draw.rectangle([160, 0, 320, 150], fill=dark_hex)
    
    # Buffer save
    buffer = io.BytesIO()
    image.save(buffer, "PNG")
    buffer.seek(0)
    
    # Prepare discord file
    file = discord.File(fp=buffer, filename="color-chip.png")
    
    embed = discord.Embed(
        title=f"🎨 Color Token: {name}",
        description="Resolved light mode (left) vs dark mode (right) values:",
        color=discord.Color.from_str(light_hex)
    )
    embed.add_field(name="☀️ Light Mode Hex", value=f"`{light_hex}`", inline=True)
    embed.add_field(name="🌙 Dark Mode Hex", value=f"`{dark_hex}`", inline=True)
    embed.set_image(url="attachment://color-chip.png")
    embed.set_footer(text="Flet Design System • v0.1.0")
    
    await ctx.send(file=file, embed=embed)

@bot.command(name="screenshot")
async def screenshot(ctx, mode: str = "light"):
    """
    Uploads the pre-rendered showcase graphics. Mode can be 'light' or 'dark'.
    """
    mode = mode.lower()
    if mode not in ["light", "dark"]:
        await ctx.send("❌ Invalid mode. Please choose `!screenshot light` or `!screenshot dark`.")
        return
        
    filename = f"assets/showcase-{mode}.png"
    if not os.path.exists(filename):
        await ctx.send(f"❌ Screenshot file '{filename}' was not found. Try run image generation locally first.")
        return
        
    file = discord.File(filename)
    embed = discord.Embed(
        title=f"📸 Interface Preview ({mode.capitalize()} Mode)",
        description="Rendering of your design system sandbox documentation application:",
        color=discord.Color.blue() if mode == "light" else discord.Color.dark_navy()
    )
    embed.set_image(url=f"attachment://showcase-{mode}.png")
    embed.set_footer(text="Flet Design System • v0.1.0")
    
    await ctx.send(file=file, embed=embed)

def start_bot():
    """
    Helper function to load tokens and block-execute the bot client.
    """
    token = os.getenv("DISCORD_BOT_TOKEN")
    if not token:
        print("❌ Error: DISCORD_BOT_TOKEN environment variable is not set inside your shell or .env file!")
        return
    bot.run(token)

if __name__ == "__main__":
    start_bot()
