import discord
from discord.ext import commands
from flask import Flask, request
import threading
import os

TOKEN = os.environ["DISCORD_BOT_TOKEN"]
GUILD_ID = int(os.environ["DISCORD_GUILD_ID"])
ROLE_ID = int(os.environ["DISCORD_ROLE_ID"])

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)
app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    username = data.get("discord_username")  # 例: "hbridge#1234"

    guild = bot.get_guild(GUILD_ID)
    member = discord.utils.find(lambda m: str(m) == username, guild.members)
    role = guild.get_role(ROLE_ID)

    if member and role:
        bot.loop.create_task(member.add_roles(role))
        return "ロール付与成功！", 200
    else:
        return f"ユーザーまたはロールが見つかりません: {username}", 400

@bot.event
async def on_ready():
    print(f"Botが起動しました: {bot.user}")

def run():
    app.run(host='0.0.0.0', port=5000)

threading.Thread(target=run).start()
bot.run(TOKEN)
