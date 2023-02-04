import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
from datetime import datetime
from pprint import pprint

months = ['janvier', 'février', 'mars', 'avril', 'mai', 'juin', 'juillet', 'août', 'septembre', 'octobre', 'novembre', 'décembre']

load_dotenv()
LOGIN = os.environ['LOGIN']
PASSWORD = os.environ['PASSWORD']

def getGrades():
    with requests.Session() as s:
        baseUrl = 'https://oasis.polytech.universite-paris-saclay.fr/'
        url1 = baseUrl + "prod/bo/core/Router/Ajax/ajax.php?targetProject=oasis_polytech_paris&route=BO\\Connection\\User::login"
        
        s.get(url1)
        login_data = {'login': LOGIN, 'password': PASSWORD, 'url': 'codepage=MYMARKS'}
        r = s.post(url1, data=login_data)

        url = baseUrl + 'prod/bo/core/Router/Ajax/ajax.php?targetProject=oasis_polytech_paris&route=BO\Layout\MainContent::load&codepage=MYMARKS'
        r = s.get(url)

        html = BeautifulSoup(r.text, 'html.parser').prettify()
        soup = BeautifulSoup(html, 'html.parser')
        
        courses_html = [
            course.find_parent('tr')
            for course in soup.find_all(class_="courseLine")
        ]
        
        courses = []
        for course_html in courses_html:
            course = {}
            
            # Subject and name of the grade
            course['subject-id'] = course_html.find_all('td')[0].find('div').text.splitlines()[1].strip()[:-2]
            course['subject'] = course_html.find_all('td')[0].find('div').text.splitlines()[3].strip()
            course['name'] = course_html.find_all('td')[1].text.strip()
            
            # Grade
            grade_str = course_html.find_all('td')[3].text.strip()
            try:
                course['grade'] = float(grade_str.replace(',', '.'))
            except ValueError:
                course['grade'] = None
                
            # Date and conversion to python datetime object
            course['date-str'] = course_html.find_all('td')[2].text.strip()
            date_list = course['date-str'].split(' ')
            course['date'] = datetime(int(date_list[2]), months.index(date_list[1]) + 1, int(date_list[0]))
            
            # Ranking
            
            
            courses.append(course)
        
        return courses

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
    
if __name__ == '__main__':
    pprint(sorted(getGrades(), key=lambda x: x['date']))
