import requests
from bs4 import BeautifulSoup
from html.parser import HTMLParser
from dotenv import load_dotenv
import os
from datetime import datetime
from pprint import pprint

load_dotenv()
LOGIN = os.getenv('LOGIN')
PASSWORD = os.getenv('PASSWORD')

months = ['janvier', 'février', 'mars', 'avril', 'mai', 'juin', 'juillet', 'août', 'septembre', 'octobre', 'novembre', 'décembre']

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
            course['subject-id'] = course_html.find_all('td')[0].find('div').text.splitlines()[1].strip()[:-2]
            course['subject'] = course_html.find_all('td')[0].find('div').text.splitlines()[3].strip()
            course['name'] = course_html.find_all('td')[1].text.strip()
            course['grade'] = course_html.find_all('td')[3].text.strip()
            course['date-str'] = course_html.find_all('td')[2].text.strip()
            date_list = course['date-str'].split(' ')
            course['date'] = datetime(int(date_list[2]), months.index(date_list[1]) + 1, int(date_list[0]))
            courses.append(course)
        
        return courses
    
if __name__ == '__main__':
    pprint(getGrades())
