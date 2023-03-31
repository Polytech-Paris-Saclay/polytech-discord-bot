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
# Peip1

# Peip2
nbr_groupes_peip2 = 4
parcours_groupes_peip2 = ['Physique','Chimie','Numérique','Numérique']
groupes_anglais = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']

''' Discord bot '''
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.command(name='updateS3')
async def updateS3(ctx):
    semester = 'S3'
    year_name = 'peip2'
    previous_year = 'peip1'

    channelinit = bot.get_channel(899980108985688065)
    guild = channelinit.guild
    previous_semester = 'S'+str(int(semester[1])-1)
    year = subjectDatabase[semester]['year']
    role_year = find(lambda r: r.name == 'PeiP 2', guild.roles)

    ''' Delete previous roles '''
    for role in guild.roles:
        if previous_semester in role.name:
            await role.delete()

    ''' Create new roles '''
    for groupe_anglais in groupes_anglais:
        await createRoleGroupeAnglais(guild, groupe_anglais, semester)
    for groupe in range(1, nbr_groupes_peip2+1):
        await createRoleGroupeTDTP(guild, groupe, semester)
    for option in subjectDatabase['S3']['options']:
        await createRoleOption(guild, option, semester)

    ''' Update channel "groupe et option peip2" '''
    await updateGroupeEtOptionChannel(guild, semester, year_name, role_year, subjectDatabase)

    ''' Archive previous categories (into '═ [Archives S2 - previous year] ═') and give permissions '''
    archive_category = await guild.create_category(name=f'═ [Archives {previous_semester} - {int(year[0])-1}/{int(year[1])-1}] ═')
    categories_to_archive = [
        f'═══ Tronc commun - {previous_semester} ═══',
        f'══════ Option - {previous_semester} ══════',
        f'════ Parcours - {previous_year} ════',
        f'════ anglais - {previous_year} ═════',
        f'═══ Groupe TD/TP - {previous_semester} ════'
    ]
    for category_name in categories_to_archive:
        await archiveThisCategory(guild, category_name, archive_category)

    ''' Create new categories with subjects channels and permissions '''
    await createCategoryTroncCommun(guild, subjectDatabase[semester]['tronc_commun'], semester, role_year)
    await createCategoryGroupeTDTP(guild, nbr_groupes_peip2, semester)
    await createCategoryOptions(guild, subjectDatabase[semester]['options'], semester)
    await createCategoryParcours(guild, subjectDatabase['S3']['parcours'], parcours_groupes_peip2, semester, year_name)
    await createCategoryAnglais(guild, groupes_anglais, semester, year_name)


@bot.command(name='updateS4')
async def updateS4(ctx):
    semester = 'S4'
    year_name = 'peip2'
    previous_year = 'peip1'

    channelinit = bot.get_channel(899980108985688065)
    guild = channelinit.guild
    previous_semester = 'S'+str(int(semester[1])-1)
    year = subjectDatabase[semester]['year']
    role_year = find(lambda r: r.name == 'PeiP 2', guild.roles)

    ''' Delete previous roles '''
    for role in guild.roles:
        if previous_semester in role.name:
            await role.delete()

    ''' Create new roles '''
    for groupe_anglais in groupes_anglais:
        await createRoleGroupeAnglais(guild, groupe_anglais, semester)
    for groupe in range(1, nbr_groupes_peip2+1):
        await createRoleGroupeTDTP(guild, groupe, semester)
    for option in subjectDatabase['S4']['options']:
        await createRoleOption(guild, option, semester)

    ''' Update channel "groupe et option peip2" '''
    await updateGroupeEtOptionChannel(guild, semester, year_name, role_year, subjectDatabase)

    ''' Archive previous categories (into '═ [Archives S3 - this year] ═') and give permissions '''
    archive_category = await guild.create_category(name=f'═ [Archives {previous_semester} - {int(year[0])}/{int(year[1])}] ═')
    categories_to_archive = [
        f'═══ Tronc commun - {previous_semester} ═══',
        f'══════ Option - {previous_semester} ══════',
        f'═══ Groupe TD/TP - {previous_semester} ════'
    ]
    for category_name in categories_to_archive:
        await archiveThisCategory(guild, category_name, archive_category)

    ''' Create new categories with subjects channels and permissions '''
    await createCategoryTroncCommun(guild, subjectDatabase[semester]['tronc_commun'], semester, role_year)
    await createCategoryGroupeTDTP(guild, nbr_groupes_peip2, semester)
    await createCategoryOptions(guild, subjectDatabase[semester]['options'], semester)

''' Tests '''
@bot.command(name='test')
async def test(ctx):
    channelinit = bot.get_channel(899980108985688065)
    guild = channelinit.guild
    print('test')

bot.run(TOKEN)