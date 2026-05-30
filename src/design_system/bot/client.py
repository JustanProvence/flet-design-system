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
import google.generativeai as genai
from PIL import Image, ImageDraw
from design_system.tokens.manager import tokens

# Load environment variables (dotenv is handled via flet or manually)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


def generate_gemini_content(prompt_content: str) -> str:
    """
    Synchronous helper querying Gemini with automatic model fallbacks.
    Tries multiple standard model IDs to prevent 404 API version errors.
    """
    models_to_try = [
        "gemini-2.5-flash",
        "gemini-1.5-flash-latest",
        "gemini-1.5-flash",
        "gemini-pro"
    ]
    last_ex = None
    for model_name in models_to_try:
        try:
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(prompt_content)
            return response.text
        except Exception as e:
            last_ex = e
            continue
    raise last_ex


async def send_in_chunks(ctx, text: str):
    """
    Sends a potentially long string to a Discord context,
    splitting it safely into chunks of up to 1900 characters
    to prevent truncation while keeping markdown formatting.
    """
    if len(text) <= 1950:
        await ctx.send(text)
        return

    lines = text.split("\n")
    current_chunk = []
    current_length = 0

    for line in lines:
        if current_length + len(line) + 1 > 1900:
            if current_chunk:
                await ctx.send("\n".join(current_chunk))
            current_chunk = [line]
            current_length = len(line)
        else:
            current_chunk.append(line)
            current_length += len(line) + 1

    if current_chunk:
        await ctx.send("\n".join(current_chunk))


async def reply_in_chunks(message, text: str):
    """Replies to a message in chunks to prevent truncation."""
    if len(text) <= 1950:
        await message.reply(text)
        return

    lines = text.split("\n")
    current_chunk = []
    current_length = 0
    first = True

    for line in lines:
        if current_length + len(line) + 1 > 1900:
            chunk_content = "\n".join(current_chunk)
            if first:
                await message.reply(chunk_content)
                first = False
            else:
                await message.channel.send(chunk_content)
            current_chunk = [line]
            current_length = len(line)
        else:
            current_chunk.append(line)
            current_length += len(line) + 1

    if current_chunk:
        chunk_content = "\n".join(current_chunk)
        if first:
            await message.reply(chunk_content)
        else:
            await message.channel.send(chunk_content)

# Setup bot intents
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=["!", "/"], intents=intents, help_command=None)


@bot.event
async def on_ready():
    """Triggered when the Discord client establishes a successful websocket connection."""
    print(f"Logged in as {bot.user.name} (ID: {bot.user.id})")
    print("------")
    # Set status presence
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name="Flet Design System (type !help)"
        )
    )


@bot.event
async def on_message(message):
    """
    Triggered on every incoming message. Handles direct mentions, DMs,
    and responses in designated channels using the Gemini API.
    """
    # Avoid responding to ourselves
    if message.author == bot.user:
        return

    # Check if the message starts with any command prefix
    starts_with_prefix = any(message.content.startswith(p) for p in ["!", "/"])

    # Check if we were mentioned, if it's a DM, or if it's a specific channel
    is_dm = isinstance(message.channel, discord.DMChannel)
    is_mention = bot.user in message.mentions
    is_assistant_channel = message.channel.name == "design-assistant" if hasattr(message.channel, "name") else False

    if (is_dm or is_mention or is_assistant_channel) and not starts_with_prefix:
        # Show typing status so the user knows the AI is composing
        async with message.channel.typing():
            # Clean up the prompt
            prompt = message.content
            if is_mention:
                prompt = prompt.replace(f"<@!{bot.user.id}>", "").replace(f"<@{bot.user.id}>", "").strip()

            # If prompt is empty, just reply with a friendly greeting
            if not prompt:
                await message.reply("👋 Hello! How can I help you design today?")
                return

            # Check if gemini is configured
            gemini_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
            if not gemini_key:
                embed = discord.Embed(
                    title="⚠️ AI Chat Config Missing",
                    description=(
                        "I would love to chat with you, but my **Gemini API Key** is not set!\n\n"
                        "### How to enable:\n"
                        "1. Get a free API Key from the [Google AI Studio](https://aistudio.google.com/).\n"
                        "2. Add it to your `.env` file:\n"
                        "```env\n"
                        "GEMINI_API_KEY=\"your_key_here\"\n"
                        "```\n"
                        "3. Restart the bot (`poetry run design-system-bot`)."
                    ),
                    color=discord.Color.orange()
                )
                await message.reply(embed=embed)
                return

            try:
                # Configure and query Gemini
                genai.configure(api_key=gemini_key)

                # Context injection to make the AI sound like the Flet Design System assistant
                system_instruction = (
                    "You are the official AI Assistant for the Flet Design System. "
                    "You are intelligent, professional, and friendly. You help users design beautiful "
                    "Python applications with Flet and align them with design tokens. "
                    "Keep your responses concise, clear, and perfectly formatted for Discord Markdown."
                )

                # Run the synchronous API call in an executor thread to prevent blocking
                reply_text = await bot.loop.run_in_executor(
                    None,
                    lambda: generate_gemini_content(
                        f"System Context: {system_instruction}\n\nUser: {prompt}"
                    )
                )

                # Send response safely in chunks to prevent truncation
                await reply_in_chunks(message, reply_text)

            except Exception as ex:
                await message.reply(f"❌ Error communicating with AI: `{str(ex)}`")

    # CRITICAL: We must call process_commands so prefix !commands continue working
    await bot.process_commands(message)


@bot.command(name="help")
async def help_command(ctx):
    """Displays the standard help commands and usages."""
    embed = discord.Embed(
        title="🎨 Flet Design System Bot",
        description="Interact and inspect your design tokens and components remotely!",
        color=discord.Color.blue()
    )
    embed.add_field(
        name="`/status` or `!status`",
        value="Checks if the local Flet web server is online at port 8550.",
        inline=False
    )
    embed.add_field(
        name="`/tokens` or `!tokens`",
        value="Lists global spacing, border-radius, and typography metadata.",
        inline=False
    )
    embed.add_field(
        name="`/color <token_name>` or `!color <token_name>`",
        value="Resolves a color token and draws a visual color chip (e.g., `/color primary`).",
        inline=False
    )
    embed.add_field(
        name="`/screenshot <light/dark>` or `!screenshot <light/dark>`",
        value="Uploads the pre-rendered showcase graphics of the Flet interface.",
        inline=False
    )
    embed.add_field(
        name="`/oc <task>` or `/opencode <task>`",
        value="Launches a fully autonomous remote AI developer loop to execute workspace tasks (e.g., `/oc run pytest`).",
        inline=False
    )
    embed.set_footer(text="Flet Design System • v0.1.0")
    await ctx.send(embed=embed)


@bot.command(name="status")
async def status(ctx):
    """Checks the local health status of the Flet web server."""
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
            embed.add_field(name="Action Required",
                            value="Run `poetry run python3 src/design_system/main.py` locally.", inline=False)

    embed.set_footer(text="Flet Design System • v0.1.0")
    await ctx.send(embed=embed)


@bot.command(name="tokens")
async def show_tokens(ctx):
    """Returns lists of typography scales, spacings, and radiuses from tokens.json."""
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
    """Resolves a semantic or primitive color and returns a dynamic color chip attachment."""
    if name is None:
        await ctx.send("❌ Please specify a color name (e.g., `!color primary` or `!color blue-600`)")
        return

    # Resolve color hex values
    light_hex = tokens.get_color(name, dark=False)
    dark_hex = tokens.get_color(name, dark=True)

    # Generate Pillow color chip image
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
    """Uploads the pre-rendered showcase graphics. Mode can be 'light' or 'dark'."""
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


@bot.command(name="opencode", aliases=["oc"])
async def remote_agent_command(ctx, *, task: str = None):
    """Launches a fully autonomous remote developer loop to execute workspace tasks."""
    if task is None:
        await ctx.send("❌ Please specify a task (e.g., `/oc run pytest` or `/oc add a button inside layout.py`)")
        return

    gemini_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not gemini_key:
        await ctx.send("❌ My Gemini API key is missing. Set `GEMINI_API_KEY` in .env first.")
        return

    # Send initial status
    status_msg = await ctx.send("🤖 **Initializing Remote AI Developer Loop...**")

    # Setup tools execution logic
    import subprocess
    import re

    def read_file(path):
        # Prevent absolute paths or directory traversal outside project directory
        clean_path = os.path.normpath(path)
        if clean_path.startswith("..") or os.path.isabs(clean_path):
            return "Error: Access denied. Paths must be relative to project root."
        try:
            with open(clean_path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            return f"Error reading file: {str(e)}"

    def write_file(path, content):
        clean_path = os.path.normpath(path)
        if clean_path.startswith("..") or os.path.isabs(clean_path):
            return "Error: Access denied. Paths must be relative to project root."
        try:
            # Ensure folder exists
            dir_name = os.path.dirname(clean_path)
            if dir_name:
                os.makedirs(dir_name, exist_ok=True)
            with open(clean_path, "w", encoding="utf-8") as f:
                f.write(content)
            return "File successfully updated."
        except Exception as e:
            return f"Error writing file: {str(e)}"

    def run_command(cmd):
        # Safe command filter: prevent interactive commands or long running commands
        if any(bad in cmd for bad in ["ssh", "sudo", "interactive", "nano", "vim", "python3 src/design_system/main.py"]):
            return "Error: Terminal command not supported remotely."
        try:
            result = subprocess.run(
                cmd, shell=True, text=True, capture_output=True, timeout=30
            )
            out = result.stdout or ""
            err = result.stderr or ""
            return f"STDOUT:\n{out}\n\nSTDERR:\n{err}"
        except subprocess.TimeoutExpired:
            return "Error: Terminal command execution timed out (exceeded 30 seconds limit)."
        except Exception as e:
            return f"Error executing command: {str(e)}"

    # Configure Gemini
    genai.configure(api_key=gemini_key)

    agent_instruction = (
        "You are 'opencode', a highly intelligent AI coding agent with remote access "
        "to a workspace directory. You can read/write files and execute terminal commands "
        "to complete the user's task. You must use these exact XML tags to trigger tools:\n\n"
        "1. To read a file:\n"
        "<read_file>path/to/file.py</read_file>\n\n"
        "2. To write or overwrite a file:\n"
        "<write_file path=\"path/to/file.py\">\n"
        "file content here\n"
        "</write_file>\n\n"
        "3. To execute a shell command (e.g. pytest, git status):\n"
        "<run_command>command to run</run_command>\n\n"
        "Rules:\n"
        "- Execute exactly ONE tool action per response.\n"
        "- Wait for the tool result before generating your next action.\n"
        "- When you are finished and have verified your work (e.g. running tests), "
        "provide a summary of modifications and do not output any more tool tags."
    )

    # We maintain a state history
    history = f"System Instructions: {agent_instruction}\n\nUser Task: {task}\n\n"

    # Loop max steps (default: 30, customizable via MAX_STEPS env var)
    try:
        max_steps = int(os.getenv("MAX_STEPS", "30"))
    except ValueError:
        max_steps = 30
    for step in range(max_steps):
        # Query model with automatic fallbacks
        model_output = await bot.loop.run_in_executor(
            None,
            lambda: generate_gemini_content(history)
        )

        # Check for tool tags
        read_match = re.search(r"<read_file>(.*?)</read_file>", model_output, re.DOTALL)
        write_match = re.search(r"<write_file\s+path=\"(.*?)\"\s*>(.*?)</write_file>", model_output, re.DOTALL)
        cmd_match = re.search(r"<run_command>(.*?)</run_command>", model_output, re.DOTALL)

        if read_match:
            filepath = read_match.group(1).strip()
            await status_msg.edit(content=f"🔍 **[Step {step+1}/{max_steps}] Reading file:** `{filepath}`...")
            result = read_file(filepath)
            history += f"\nModel:\n{model_output}\n\nTool Execution Result (read_file):\n{result}\n"

        elif write_match:
            filepath = write_match.group(1).strip()
            content = write_match.group(2)
            await status_msg.edit(content=f"✏️ **[Step {step+1}/{max_steps}] Modifying file:** `{filepath}`...")
            result = write_file(filepath, content)
            history += f"\nModel:\n{model_output}\n\nTool Execution Result (write_file):\n{result}\n"

        elif cmd_match:
            cmd = cmd_match.group(1).strip()
            await status_msg.edit(content=f"💻 **[Step {step+1}/{max_steps}] Running command:** `{cmd}`...")
            result = run_command(cmd)
            # Truncate result if too long for history context
            if len(result) > 2500:
                result = result[:2500] + "... (output truncated)"
            history += f"\nModel:\n{model_output}\n\nTool Execution Result (run_command):\n{result}\n"

        else:
            # No tool matched, meaning the agent has finished!
            await status_msg.edit(content=f"✅ **Task Completed in {step} steps!**")
            await send_in_chunks(ctx, model_output)
            return

    await status_msg.edit(content=f"⚠️ **Task exceeded the maximum of {max_steps} autonomous execution steps.**")


def start_bot():
    """Helper function to load tokens and block-execute the bot client."""
    token = os.getenv("DISCORD_BOT_TOKEN")
    if not token:
        print("❌ Error: DISCORD_BOT_TOKEN environment variable is not set inside your shell or .env file!")
        return
    bot.run(token)


if __name__ == "__main__":
    start_bot()
