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
import json

from oasis import getSubjects

load_dotenv()
LOGIN = os.environ['LOGIN']
PASSWORD = os.environ['PASSWORD']
TOKEN = os.environ['TOKEN']

# year, first_semester, second_semester, subjects_first_semester, subjects_second_semester = getSubjects()
# semester_index = int(input('Numéro du semestre à update :'))

with open('subjectDatabase.json','r') as f:
    subjectDatabase = json.load(f)

''' Discord bot '''
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.command(name='s3Update')
async def s3Update(ctx):
    nbr_groupes = 4
    groupes_anglais = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']

    channelinit = bot.get_channel(899980108985688065)
    guild = channelinit.guild
    role_peip2 = find(lambda r: r.name == 'PeiP 2', guild.roles)

    ''' Create new roles and update channel "groupe et option peip2" '''
    #WIP

    ''' Archive previous categories'''
    # tronc commun

    # options

    # parcours

    # anglais

    # groupes TD/TP

    ''' Create new categories with subjects channels and permissions '''
    # tronc commun 
    tronc_commun = subjectDatabase['S3']['tronc_commun']
    category = await guild.create_category(name='═══ Tronc commun - S3 ═══')
    await category.set_permissions(guild.default_role, read_messages=False)
    await category.set_permissions(role_peip2, read_messages=True)
    for subject in tronc_commun:
        await category.create_text_channel(name=f'{subject}')
    # options
    options = subjectDatabase['S3']['options']
    category = await guild.create_category(name='══════ Option - S3 ══════')
    await category.set_permissions(guild.default_role, read_messages=False)
    await category.set_permissions(role_peip2, read_messages=True)
    for subject in options:
        await category.create_text_channel(name=f'{subject}')
    # parcours
    parcours = subjectDatabase['S3']['parcours']
    category = await guild.create_category(name='════ Parcours - S3 ════')
    await category.set_permissions(guild.default_role, read_messages=False)
    await category.set_permissions(role_peip2, read_messages=True)
    for subject in parcours:
        await category.create_text_channel(name=f'{subject}')
    # anglais
    category = await guild.create_category(name='════ anglais - peip2 ═════')
    await category.set_permissions(guild.default_role, read_messages=False)
    for groupe in groupes_anglais:
        channel = await category.create_text_channel(name=f'groupe {groupe}')
        await channel.set_permissions(find(lambda r: r.name == f'Anglais groupe {groupe} - S3', guild.roles), read_messages=True)
    # groupes TD/TP
    category = await guild.create_category(name='═══ Groupe TD/TP - S3 ════')
    await category.set_permissions(guild.default_role, read_messages=False)
    for i in range(1, nbr_groupes+1):
        channel = await category.create_text_channel(name=f'groupe {i}')
        await channel.set_permissions(find(lambda r: r.name == f'Groupe {i} - S3', guild.roles), read_messages=True)
    

@bot.command(name='test')
async def test(ctx):
    channelinit = bot.get_channel(899980108985688065)
    guild = channelinit.guild
    print('test')
    # category = await guild.create_category(name=f'test')
    # user = discord.utils.get(ctx.guild.members, name='Florian M')
    # role = find(lambda r: r.name == 'PeiP 2', guild.roles)
    # print(role)
    # await category.set_permissions(role, read_messages=True)
    # await category.create_text_channel(name=f'test')

    # role = find(lambda r: r.name == 'Visiteur', guild.roles)
    # print(role)
    # print(type(role))


''' Tests '''

bot.run(TOKEN)