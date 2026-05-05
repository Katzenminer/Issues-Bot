import discord
import secret
import requests
from discord.ext import commands

# === CONFIG ===
GITHUB_TOKEN = secret.gitToken #YOUR_GITHUB_TOKEN
OWNER = "Katzenminer"
REPO = "Issues-Bot"

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.command()
async def createissue(ctx):
    if not isinstance(ctx.channel, discord.Thread):
        await ctx.send("This command must be used inside a thread.")
        return

    thread = ctx.channel
    title = thread.name

    try:
        starter_message = await thread.fetch_message(thread.id)
        body = starter_message.content or "[No text content]"
        body += f"\n\n[Discord Thread]({thread.jump_url})"

        body_parts = []


        body_parts.append(starter_message.content or "[No text content]")

        # Attachments (images/files)
        for attachment in starter_message.attachments:
            body_parts.append(f"\n![attachment]({attachment.url})")

        # Embeds (images from links)
        for embed in starter_message.embeds:
            if embed.image and embed.image.url:
                body_parts.append(f"\n![embed]({embed.image.url})")
            if embed.thumbnail and embed.thumbnail.url:
                body_parts.append(f"\n![thumbnail]({embed.thumbnail.url})")


        body_parts.append(f"\n\n[Discord Thread]({thread.jump_url})")

        body = "\n".join(body_parts)
    except Exception:
        body = "[Could not fetch starter message]"

    # GitHub API request
    url = f"https://api.github.com/repos/{OWNER}/{REPO}/issues"
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }
    data = {
        "title": title,
        "body": body
    }

    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 201:
        issue = response.json()
        await ctx.send(f"✅ Issue created: {issue['html_url']}")
    else:
        await ctx.send(f"❌ Failed: {response.status_code}\n{response.text}")

bot.run(secret.Token)