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

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)





### TESTS ###

year, first_semester, second_semster, subjects_first_semester, subjects_second_semester = getSubjects()

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