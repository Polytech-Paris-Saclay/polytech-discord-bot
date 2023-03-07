import discord
from discord.ext import commands
from discord.ext import tasks
from discord.utils import find

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

def formCategoriesPeip2(semester_index,first_semester,second_semester,subjects_first_semester, subjects_second_semester):
    # tronc commun : UE 2 et 3 + UE1 except anglais
    tronc_commun = []
    if semester_index == first_semester:
        tronc_commun.extend(subjects_first_semester[2])
        tronc_commun.extend(subjects_first_semester[1])
        tronc_commun.extend(subjects_first_semester[0][1:]) if len(subjects_first_semester[0][1:]) > 1 else None 
    elif semester_index == second_semester:
        tronc_commun.extend(subjects_second_semester[2])
        tronc_commun.extend(subjects_second_semester[1])
        tronc_commun.extend(subjects_first_semester[0][1:]) if len(subjects_first_semester[0][1:]) > 1 else None 

    # options : UE 4 except 3 last subjects
    options = []
    if semester_index == first_semester:
        options.extend(subjects_first_semester[3][:-3])
    if semester_index == second_semester:
        options.extend(subjects_second_semester[3][:-3])
    
    # parcours : last 3 subjects of UE 4
    parcours = []
    if semester_index == first_semester:
        parcours.extend(subjects_first_semester[3][-3:])
    
    return tronc_commun, options, parcours



''' Check in console if the subjects are well extracted, and ask for the semester '''
year, first_semester, second_semester, subjects_first_semester, subjects_second_semester = getSubjects()

print('Année :',year,'\n\n')
print('Semestre :',first_semester,'\n')
for i in range(len(subjects_first_semester)):
    print('UE',i+1,':',subjects_first_semester[i])
print('\n\n','Semestre :',second_semester,'\n')
for i in range(len(subjects_second_semester)):
    print('UE',i+1,':',subjects_second_semester[i])
print('\n\n')

well_extracted = input('Correct ? (y/n)')
if well_extracted == 'n':
    exit()

semester_index = int(input('Numéro du semestre :'))

tronc_commun, options, parcours = formCategoriesPeip2(semester_index,first_semester,second_semester,subjects_first_semester, subjects_second_semester)

print(tronc_commun)
print(options)
print(parcours)

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
    
    ''' Archive previous categories'''
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