import discord
from discord.ext import commands
from discord.ext import tasks
from discord.utils import find
from discord import app_commands

from dotenv import load_dotenv
import re
import os

load_dotenv()
TOKEN = os.environ['TOKEN']
AGENDA_URL = os.environ['AGENDA_URL']

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.command(name='updateInfo')
async def update_chapters(ctx, channel: discord.TextChannel):
    os.chdir('infoChannelUpdate')
    with open('infoChannel.md', 'r', encoding='utf-8') as f:
        markdown_file = f.read()
    sections = re.split(r'\n##\s+', markdown_file)
    chapter_parts = []
    for section in sections:
        title, description = section.split('\n', 1)
        #remove the ## before the title
        title = title[2:] if title[0] == '#' else title
        chapter_parts.append({'title': title, 'description': description})
    channel = bot.get_channel(1122874143596089354)
    await channel.purge()
    for part in chapter_parts:
        embed = discord.Embed(title=part['title'], description=part['description'],color=0x00A8E8)
        await channel.send(embed=embed)


bot.run(TOKEN)
