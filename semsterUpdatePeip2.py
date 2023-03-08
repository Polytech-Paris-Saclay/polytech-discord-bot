import discord
from discord.ext import commands
from discord.ext import tasks
from discord.utils import find
from discord import app_commands

from dotenv import load_dotenv
import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
from lxml import etree

from oasis import getSubjects

load_dotenv()
LOGIN = os.environ['LOGIN']
PASSWORD = os.environ['PASSWORD']
TOKEN = os.environ['TOKEN']

year, first_semester, second_semester, subjects_first_semester, subjects_second_semester = getSubjects()
semester_index = int(input('Numéro du semestre :'))

''' Discord bot '''
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.command(name='test')
async def semesterUpdatePEIP2(ctx):
    if semester_index != first_semester:
        print("Le semestre n'est pas celui renseigné")
    print('test')
    channel = bot.get_channel(899980108985688065)
    guild = channel.guild
    
    ''' Archive previous categories '''
    # tronc commun

    # options

    # parcours

    # anglais

    ''' Create new categories with subjects and permissions '''
    # tronc commun 

    # options

    # parcours

    # anglais

''' Tests '''

bot.run(TOKEN)