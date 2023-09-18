from bs4 import BeautifulSoup

def getSubjectsFromHTML(filename):
    with open(filename, 'r') as f:
        html = f.read()
        soup = BeautifulSoup(html, 'html.parser') 
    
    header_year_info = soup.find_all(class_="SemesterPanel col-lg-12")[0].find_all('h2')[0].text.split(' ')

    year = [elem for elem in header_year_info if elem.startswith('20')]
    
    first_semester = int(header_year_info[header_year_info.index('semestre') - 1][0])
    second_semester = int(header_year_info[header_year_info.index('semestre') - 1][0]) + 1

    specialite = header_year_info[4].split('-')[1]
    match specialite:
        case 'PHOT': specialite = 'PSO'
        case 'INFO': specialite = 'INFO'
        case 'MTX': specialite = 'MTX'
        case 'ESR': specialite = 'ESR'
        case _: specialite = None

    list_UE = [
        ue_html.find_all('td')
        for ue_html in soup.find_all(class_="moduleBox")
    ]
    
    # formatting
    for ue in list_UE:
        for i in range(len(ue)):
            ue[i] = ue[i].text.strip().encode('cp1252').decode('utf8')

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

    return year, first_semester, second_semester, subjects_first_semester, subjects_second_semester, specialite

year, first_semester, second_semester, subjects_first_semester, subjects_second_semester, specialite = getSubjectsFromHTML('APP3_INFO_23-24.html')
print(year, specialite, first_semester, second_semester, subjects_first_semester, subjects_second_semester)