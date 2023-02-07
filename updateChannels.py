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

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)


year, first_semester, second_semster, subjects_first_semester, subjects_second_semester = getSubjects()

''' Check in console if the subjects are well extracted '''
print('Année :')
print(year,'\n\n\n')

print('Semestre :')
print(first_semester,'\n')
for i in range(len(subjects_first_semester)):
    print('UE',i+1,':',subjects_first_semester[i])

print('\n\n\n','Semestre :')
print(second_semster,'\n')
for i in range(len(subjects_second_semester)):
    print('UE',i+1,':',subjects_second_semester[i])
print('\n\n\n')

well_extracted = input('Correct ? (y/n)')
if well_extracted == 'n':
    exit()


''' Get list of categories '''
categories = []
# code

''' Archive 'troncs communs', 'groupes', 'options' categories '''
#code

''' transform subject list into correct groups to build categories '''
#code

''' Create channels for each subject in categories with semester number '''
#code



# bot.run(TOKEN)