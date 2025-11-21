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
    input_name = data.get("display_name") or data.get("discord_username")  # どちらでも受け付け

    print(f"受け取った名前: {input_name}")

    guild = bot.get_guild(GUILD_ID)
    if not guild:
        return "ギルドが見つかりません", 500

    # メンバー全件取得（キャッシュにいない可能性対策）
    bot.loop.create_task(guild.chunk())

    # ユーザー名 or 表示名でマッチするメンバーを検索
    member = discord.utils.find(
        lambda m: str(m) == input_name or m.display_name == input_name,
        guild.members
    )

    role = guild.get_role(ROLE_ID)

    if member and role:
        bot.loop.create_task(member.add_roles(role))
        print(f"ロールを付与しました: {member}")
        return "ロール付与成功！", 200
    else:
        print(f"ユーザーまたはロールが見つかりません: {input_name}")
        return f"ユーザーまたはロールが見つかりません: {input_name}", 400

@bot.event
async def on_ready():
    print(f"Botが起動しました: {bot.user}")

def run():
    app.run(host='0.0.0.0', port=5000)

threading.Thread(target=run).start()
bot.run(TOKEN)

