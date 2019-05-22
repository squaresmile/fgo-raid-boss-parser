import os
from datetime import timezone, timedelta
import discord
import aiohttp
import aiofiles

CHANNEL = "jp-event-raid"
USER = "solution"

client = discord.Client()

with open("discord_api_token.txt") as f:
    discord_api_token = f.read().strip()
if not os.path.exists("screenshots"):
    os.mkdir("screenshots")


async def download_raid_screenshots(time, user, url, file_name):
    print(f"{time:%Y-%m-%d %H:%M:%S}|{user}|{url}")
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                async with aiofiles.open(f"screenshots/{user}/{file_name}", mode="wb") as file:
                    content = await response.content.read()
                    await file.write(content)
                    await file.flush()

@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")

@client.event
async def on_message(message):
    if str(message.channel.name) == CHANNEL:
        if message.attachments:
            user = str(message.author.display_name)
            time = message.created_at.replace(tzinfo=timezone.utc).astimezone(tz=None)
            # if user == USER:
            created_time = message.created_at + timedelta(hours=-7)
            file_name = f"Screenshot_{created_time:%Y%m%d-%H%M%S}.png"
            for attachment in message.attachments:
                await download_raid_screenshots(time, user, attachment.url, file_name)

client.run(discord_api_token)
