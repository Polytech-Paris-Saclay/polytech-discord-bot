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


load_dotenv()
LOGIN = os.environ['LOGIN']
PASSWORD = os.environ['PASSWORD']

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

def getSubjects():
    with requests.Session() as s:
        baseUrl = 'https://oasis.polytech.universite-paris-saclay.fr/'
        url1 = baseUrl + "prod/bo/core/Router/Ajax/ajax.php?targetProject=oasis_polytech_paris&route=BO\\Connection\\User::login"
        
        s.get(url1)
        login_data = {
            'login': LOGIN, 
            'password': PASSWORD, 
            'url': 'codepage=MYCHOICES'
        }
        r = s.post(url1, data=login_data)

        url = baseUrl + 'prod/bo/core/Router/Ajax/ajax.php?targetProject=oasis_polytech_paris&route=BO\Layout\MainContent::load&codepage=MYCHOICES'

        r = s.get(url)
        html = BeautifulSoup(r.text, 'html.parser').prettify()
        soup = BeautifulSoup(html, 'html.parser')
        dom = etree.HTML(str(soup))
        
        header_year_info = soup.find_all(class_="SemesterPanel col-lg-12")[0].find_all('h2')[0].text.split(' ')

        year = [elem for elem in header_year_info if elem.startswith('20')]
        
        first_semester = int(header_year_info[header_year_info.index('semestre\n') - 1][0])
        second_semster = int(header_year_info[header_year_info.index('semestre\n') - 1][0]) + 1

        list_UE = [
            ue_html.find_all('td')
            for ue_html in soup.find_all(class_="moduleBox")
        ]
        
        # formatting
        for ue in list_UE:
            for i in range(len(ue)):
                ue[i] = ue[i].text.strip()

        

        subjects_first_semester = []

        index_next_semester = 0
        for i in range(len(list_UE)):
            temp = []
            for j in range (len(list_UE[i])):
                if list_UE[i][j] == 'Inscrit':
                    temp.append(list_UE[i][j-3])
                if list_UE[i][j].startswith('Anglais') and i > 0:
                    index_next_semester = i
                    break
            if index_next_semester != 0:
                break
            subjects_first_semester.append(temp)



        subjects_second_semester = []

        for i in range(index_next_semester, len(list_UE)):
            temp = []
            for j in range (len(list_UE[i])):
                if list_UE[i][j] == 'Inscrit':
                    temp.append(list_UE[i][j-3])
            subjects_second_semester.append(temp)

    return year, first_semester, second_semster, subjects_first_semester, subjects_second_semester



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