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
from semesterUpdateFunctions import *

load_dotenv()
LOGIN = os.environ['LOGIN']
PASSWORD = os.environ['PASSWORD']
TOKEN = os.environ['TOKEN']

''' Load subjectDatabase '''
with open('subjectDatabase.json','r',encoding="utf-8") as f:
    subjectDatabase = json.load(f)

''' Manual Variables '''
nbr_groupes = 4
parcours_groupes = ['Physique','Chimie','Numérique','Numérique']
groupes_anglais = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']

''' Discord bot '''
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.command(name='updateS3')
async def updateS3(ctx):
    pass

@bot.command(name='updateS4')
async def updateS4(ctx):
    channelinit = bot.get_channel(899980108985688065)
    guild = channelinit.guild

    semester = 'S4'
    year_name = 'peip2'
    year = subjectDatabase[semester]['year']
    role_year = find(lambda r: r.name == 'PeiP 2', guild.roles)

    ''' Delete S3 roles '''
    for role in guild.roles:
        if 'S3' in role.name:
            await role.delete()

    ''' Create new roles '''
    for groupe_anglais in groupes_anglais:
        await createRoleGroupeAnglais(guild, groupe_anglais, semester)
    for groupe in range(1, nbr_groupes+1):
        await createRoleGroupeTDTP(guild, groupe, semester)
    for option in subjectDatabase['S4']['options']:
        await createRoleOption(guild, option, semester)

    ''' Update channel "groupe et option peip2" '''
    await updateGroupeEtOptionChannel(guild, semester, year_name, role_year, subjectDatabase)

    ''' Archive previous categories (into '═ [Archives S3 - this year] ═') and give permissions '''
    previous_semester = 'S'+str(int(semester[1])-1)
    archive_category = await guild.create_category(name=f'═ [Archives {previous_semester} - {int(year[0])}/{int(year[1])}] ═')
    categories_to_archive = [
        f'═══ Tronc commun - {previous_semester} ═══',
        f'══════ Option - {previous_semester} ══════',
        f'═══ Groupe TD/TP - {previous_semester} ════'
    ]
    for category_name in categories_to_archive:
        await archiveThisCategory(guild, category_name, archive_category)

    ''' Create new categories with subjects channels and permissions '''
    # tronc commun 
    tronc_commun = subjectDatabase['S4']['tronc_commun']
    category = await guild.create_category(name='═══ Tronc commun - S4 ═══', position=4)
    await category.set_permissions(guild.default_role, read_messages=False)
    await category.set_permissions(role_year, read_messages=True)
    for subject in tronc_commun:
        await category.create_text_channel(name=f'{subject}')
    # groupes TD/TP
    category = await guild.create_category(name='═══ Groupe TD/TP - S4 ════', position=4)
    await category.set_permissions(guild.default_role, read_messages=False)
    for i in range(1, nbr_groupes+1):
        channel = await category.create_text_channel(name=f'groupe {i}')
        await channel.set_permissions(find(lambda r: r.name == f'Groupe {i} - S4', guild.roles), read_messages=True)
    # options
    options = subjectDatabase['S4']['options']
    category = await guild.create_category(name='══════ Option - S4 ══════', position=4)
    await category.set_permissions(guild.default_role, read_messages=False)
    for subject in options:
        channel = await category.create_text_channel(name=f'{subject[0]}')
        await channel.set_permissions(find(lambda r: r.name == f'{subject[0]} - S4', guild.roles), read_messages=True) 

''' Tests '''
@bot.command(name='test')
async def test(ctx):
    channelinit = bot.get_channel(899980108985688065)
    guild = channelinit.guild
    print('test')

bot.run(TOKEN)