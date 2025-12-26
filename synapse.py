import discord
from discord.ext import commands
from discord.ui import View, button
from discord import app_commands
import re
import random
import os
import json
import time

# =========================
# DISCORD SETUP
# =========================
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# =========================
# FILE PATHS
# =========================
SERVER_SETTINGS_FILE = "server_settings.json"
SERVER_SWEARS_FILE = "server_swears.json"

# =========================
# BASE SWEARS (GLOBAL)
# =========================
bad_words = [#put your words here
]

# =========================
# PUBLIC REPLIES
# =========================
savage_replies = [#add replies here

]

# =========================
# SETTINGS HELPERS
# =========================
def load_json(path):
    if not os.path.exists(path):
        return {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = f.read().strip()
            return json.loads(data) if data else {}
    except:
        return {}

def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def replies_enabled(guild_id):
    settings = load_json(SERVER_SETTINGS_FILE)
    return settings.get(str(guild_id), {}).get("replies", True)

# =========================
# SERVER SWEARS
# =========================
def get_server_swears(guild_id):
    return load_json(SERVER_SWEARS_FILE).get(str(guild_id), [])

# =========================
# NORMALIZE TEXT
# =========================
def normalize_text(text):
    text = re.sub(r"[^\w\s]", "", text)
    text = re.sub(r"(.)\1{2,}", r"\1\1", text)
    return text.lower()

# =========================
# REGEX BUILDER
# =========================
def build_regex_for_guild(guild_id):
    words = bad_words + get_server_swears(guild_id)
    regex_list = []

    for word in words:
        escaped = re.escape(word)
        escaped = escaped.replace(r"\*", r"[\W_]*")
        regex_list.append(
            re.compile(rf"\b{escaped}\b", re.IGNORECASE)
        )
    return regex_list

# =========================
# WARNING COOLDOWN
# =========================
last_warned = {}

def can_warn(user_id, cooldown=30):
    now = time.time()
    if user_id in last_warned and now - last_warned[user_id] < cooldown:
        return False
    last_warned[user_id] = now
    return True

# =========================
# BAN BUTTON
# =========================
class BanButtonView(View):
    def __init__(self, user):
        super().__init__(timeout=None)
        self.user = user

    @button(label="🔨 Ban User", style=discord.ButtonStyle.danger)
    async def ban(self, interaction: discord.Interaction, _):
        if not interaction.user.guild_permissions.ban_members:
            return await interaction.response.send_message(
                "❌ No permission.", ephemeral=True
            )
        await interaction.guild.ban(self.user, reason="SYNAPSE Auto-Mod")
        await interaction.response.send_message("✅ User banned.", ephemeral=True)

# =========================
# EVENTS
# =========================
@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"✅ SYNAPSE online as {bot.user}")

    # >>> ADDED <<< ACTIVE SERVER LOG
    print("\n" + "=" * 50)
    print("ACTIVE SERVERS")
    print("=" * 50)
    for guild in bot.guilds:
        print(f"Server Name : {guild.name}")
        print(f"Server ID   : {guild.id}")
        print(f"Members    : {guild.member_count}")
        print("-" * 50)
    print("=" * 50 + "\n")

@bot.event
async def on_guild_join(guild):
    # >>> ADDED <<< LOG NEW SERVER
    print(f"🆕 Joined new server: {guild.name} | ID: {guild.id}")

@bot.event
async def on_message(message):
    if message.author.bot or not message.guild:
        return

    cleaned = normalize_text(message.content)
    regex_list = build_regex_for_guild(message.guild.id)

    for pattern in regex_list:
        if pattern.search(cleaned):

            try:
                await message.delete()
            except:
                pass

            if can_warn(message.author.id):
                embed = discord.Embed(
                    title="⚠️ Warning Issued",
                    description=(
                        "Your message was removed because it contained "
                        "**abusive or inappropriate language**.\n\n"
                        "**Repeated violations may result in a ban.**"
                    ),
                    color=discord.Color.orange()
                )
                embed.add_field(
                    name="Message Content",
                    value=message.content or "`<empty>`",
                    inline=False
                )
                embed.set_footer(text="SYNAPSE Auto-Moderation")

                try:
                    await message.author.send(embed=embed)
                except:
                    pass

            if replies_enabled(message.guild.id):
                await message.channel.send(
                    f"{message.author.mention} {random.choice(savage_replies)}"
                )

            return

    await bot.process_commands(message)

# =========================
# SLASH COMMANDS (UNCHANGED)
# =========================
@bot.tree.command(name="replies")
@app_commands.default_permissions(administrator=True)
async def replies(interaction: discord.Interaction, mode: str):
    mode = mode.lower()
    data = load_json(SERVER_SETTINGS_FILE)
    data.setdefault(str(interaction.guild.id), {})["replies"] = (mode == "on")
    save_json(SERVER_SETTINGS_FILE, data)
    await interaction.response.send_message(
        f"✅ Replies **{mode.upper()}**.", ephemeral=True
    )

# =========================
# RUN
# =========================
bot.run("Your code here")
