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

from semesterUpdateFunctions import *

load_dotenv()
TOKEN = os.environ['TOKEN']

''' Load subjectDatabase '''
with open('subjectDatabase.json','r',encoding="utf-8") as f:
    subjectDatabase = json.load(f)

''' Load semesterUpdateInstructions '''
os.chdir('semesterUpdate')
with open('semesterUpdateInstructions.json','r',encoding="utf-8") as f:
    semesterUpdateInstructions = json.load(f)

''' Discord bot '''
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.command(name='update')
# !update <semester>
# uses semesters instructions in semesterUpdateInstructions
async def semesterUpdate(ctx, semester: str):
    channelinit = bot.get_channel(899980108985688065)
    guild = channelinit.guild

    year_name = next((key for key in semesterUpdateInstructions if semester in semesterUpdateInstructions[key]), '')
    if not year_name:
        await ctx.send(f'Erreur: le semestre {semester} n\'existe pas.')
        return None

    role_discord_year = semesterUpdateInstructions[year_name]['role_discord_year']
    role_year = find(lambda r: r.name == role_discord_year, guild.roles)
    year = subjectDatabase[semester]['year']
    previous_year = semesterUpdateInstructions[year_name]['previous_year']
    previous_semester = 'S'+ str(int(semester[1:])-1) if semester[1:] != '10' else 'S9'

    nbr_groupes = semesterUpdateInstructions[year_name]['nbr_groupes'] if 'nbr_groupes' in semesterUpdateInstructions[year_name] else None
    parcours_groupes = semesterUpdateInstructions[year_name]['parcours_groupes'] if 'parcours_groupes' in semesterUpdateInstructions[year_name] else None
    groupes_anglais = semesterUpdateInstructions[year_name]['groupes_anglais'] if 'groupes_anglais' in semesterUpdateInstructions[year_name] else None
    

    print(semesterUpdateInstructions[year_name][semester])

    for instruction_name, instructions in semesterUpdateInstructions[year_name][semester].items():
        match instruction_name:
            case "delete_previous_roles": await deletePreviousRoles(guild, previous_semester) if instructions else None
            case "create_new_roles": await createNewRoles(guild, semester, instructions, nbr_groupes, groupes_anglais, subjectDatabase)
            case "update_groupeEtOption_channel" : await updateGroupeEtOptionChannel(guild, semester, year_name, role_year, subjectDatabase) if instructions else None
            case "archive_previous_categories" : await archivePreviousCategories(guild, previous_semester, year, previous_year, instructions)
            case "create_new_categories" : await createNewCategories(guild, semester, instructions, role_year, nbr_groupes, parcours_groupes, groupes_anglais, year_name, subjectDatabase)

@bot.command(name='tempdelete')
# debug command
async def default(ctx):
    guild = ctx.guild
    categories = [
        find(lambda c: c.name == '═══ Groupe TD/TP - S2 ════', guild.categories),
        find(lambda c: c.name == '══════ Option - S2 ══════', guild.categories),
        find(lambda c: c.name == '═══ Tronc commun - S2 ═══', guild.categories),
        find(lambda c: c.name == '════ parcours - peip1 ════', guild.categories),
        find(lambda c: c.name == '════ anglais - peip1 ═════', guild.categories)
    ]
    for category in categories:
        # delete every channel in the category
        for channel in category.channels:
            await channel.delete()
        # delete the category
        await category.delete()

bot.run(TOKEN)