import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True  # REQUIRED

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.command()
async def createissue(ctx):
    # Ensure command is used inside a thread
    if not isinstance(ctx.channel, discord.Thread):
        await ctx.send("This command must be used inside a thread.")
        return

    thread = ctx.channel

    # Thread title
    title = thread.name

    # Get starter message (thread's first message)
    try:
        starter_message = await thread.fetch_message(thread.id)
        body = starter_message.content
    except Exception:
        body = "Could not fetch starter message."

    # Output (you can replace this with your own processing logic)
    response = f"**Title:** {title}\n**Body:** {body}"
    await ctx.send(response)


bot.run("YOUR_BOT_TOKEN")