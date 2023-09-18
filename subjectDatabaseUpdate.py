import json
from getSubjectsWithHTML import getSubjectsFromHTML

def formCategoriesPEIP(year, first_semester, second_semester, subjects_first_semester, subjects_second_semester):
    '''first_semester'''
    first_semester_name = 'S' + str(first_semester)
    # tronc commun : UE 1, 2 + UE0 except anglais
    tronc_commun = []
    tronc_commun.extend(subjects_first_semester[2])
    tronc_commun.extend(subjects_first_semester[1])
    tronc_commun.extend(subjects_first_semester[0][1:]) if len(subjects_first_semester[0][1:]) > 1 else None 
    # options : UE 3 except 3 last subjects, and add a blank space for the associated emoji
    options = []
    for option in subjects_first_semester[3][:-3]:
        options.append([option, ''])
    # parcours : last 3 subjects of UE 3
    parcours = []
    parcours.extend(subjects_first_semester[3][-3:])
    
    globals()[first_semester_name] = {
        'year': year,
        'tronc_commun': tronc_commun,
        'options': options,
        'parcours': parcours
    }
    '''second_semester'''
    second_semester_name = 'S' + str(second_semester)
    # tronc commun : UE 1, 2 + UE0 except anglais
    tronc_commun = []
    tronc_commun.extend(subjects_second_semester[2])
    tronc_commun.extend(subjects_second_semester[1])
    tronc_commun.extend(subjects_second_semester[0][1:]) if len(subjects_second_semester[0][1:]) > 1 else None
    # options : UE 3 except 3 last subjects, and add a blank space for the associated emoji
    options = []
    for option in subjects_second_semester[3][:-3]:
        options.append([option, ''])
    # parcours : last 3 subjects of UE 3
    parcours = []
    parcours.extend(subjects_second_semester[3][-3:])
    globals()[second_semester_name] = {
        'year': year,
        'tronc_commun': tronc_commun,
        'options': options,
        'parcours': parcours
    }
    ''' Save '''
    with open('subjectDatabase.json','r', encoding='utf-8') as f:
        data = json.load(f)
    data[first_semester_name] = globals()[first_semester_name]
    data[second_semester_name] = globals()[second_semester_name]
    with open('subjectDatabase.json','w', encoding='utf-8') as f:
        json.dump(data,f)

# WIP
def formCategoriesET3(year, first_semester, second_semester, subjects_first_semester, subjects_second_semester):
    '''first_semester'''
    first_semester_name = 'S' + str(first_semester)
    # tronc commun : UE 2, 3 + UE1 except anglais
    tronc_commun = []
    tronc_commun.extend(subjects_first_semester[2])
    tronc_commun.extend(subjects_first_semester[1])
    tronc_commun.extend(subjects_first_semester[0][1:]) if len(subjects_first_semester[0][1:]) > 1 else None 
    # options : UE 4 except 3 last subjects, and add a blank space for the associated emoji
    options = []
    for option in subjects_first_semester[3][:-3]:
        options.append([option, ''])
    # parcours : last 3 subjects of UE 4
    parcours = []
    parcours.extend(subjects_first_semester[3][-3:])
    
    globals()[first_semester_name] = {
        'year': year,
        'tronc_commun': tronc_commun,
        'options': options,
        'parcours': parcours
    }
    '''second_semester'''
    second_semester_name = 'S' + str(second_semester)
    # tronc commun : UE 2, 3 + UE1 except anglais
    tronc_commun = []
    tronc_commun.extend(subjects_second_semester[2])
    tronc_commun.extend(subjects_second_semester[1])
    tronc_commun.extend(subjects_second_semester[0][1:]) if len(subjects_second_semester[0][1:]) > 1 else None
    # options : UE 4 except 3 last subjects, and add a blank space for the associated emoji
    options = []
    for option in subjects_second_semester[3][:-3]:
        options.append([option, ''])
    # parcours : last 3 subjects of UE 4
    parcours = []
    parcours.extend(subjects_second_semester[3][-3:])
    globals()[second_semester_name] = {
        'year': year,
        'tronc_commun': tronc_commun,
        'options': options,
        'parcours': parcours
    }
    ''' Save '''
    with open('subjectDatabase.json','r', encoding='utf-8') as f:
        data = json.load(f)
    data[first_semester_name] = globals()[first_semester_name]
    data[second_semester_name] = globals()[second_semester_name]
    with open('subjectDatabase.json','w', encoding='utf-8') as f:
        json.dump(data,f)

def formCategoriesAPP3(year, first_semester, second_semester, subjects_first_semester, subjects_second_semester, specialite):
    # tronc commun app : UE0 3rd subject + UE1 + UE2 +UE3
    tronc_commun_app = []
    tronc_commun_app.extend(subjects_first_semester[1])
    tronc_commun_app.extend(subjects_first_semester[2])
    tronc_commun_app.extend(subjects_first_semester[3])
    tronc_commun_app.append(subjects_first_semester[0][2])
    # specialite_app : UE,4,5,6,7
    specialite_app = []
    specialite_app.extend(subjects_first_semester[4])
    specialite_app.extend(subjects_first_semester[5])
    specialite_app.extend(subjects_first_semester[6])
    specialite_app.extend(subjects_first_semester[7])
    
    ''' Save '''
    with open('subjectDatabase.json','r', encoding='utf-8') as f:
        data = json.load(f)
    data[f'S{first_semester}']['year'] = year
    data[f'S{first_semester}']['tronc_commun_app'] = tronc_commun_app
    data[f'S{first_semester}'][f'specialite_app_{specialite}'] = specialite_app
    with open('subjectDatabase.json','w', encoding='utf-8') as f:
        json.dump(data,f)

# add the specialite subjects that are missing with other oasis files from other specialites students
def addSpecialiteAPP(first_semester, second_semester, specialite):
    # specialite_app : UE,4,5,6,7
    specialite_app = []
    specialite_app.extend(subjects_first_semester[4])
    specialite_app.extend(subjects_first_semester[5])
    specialite_app.extend(subjects_first_semester[6])
    specialite_app.extend(subjects_first_semester[7])

    ''' Save '''
    with open('subjectDatabase.json','r', encoding='utf-8') as f:
        data = json.load(f)
    # add the found specialite_app to the database
    data[f'S{first_semester}'][f'specialite_app_{specialite}'] = specialite_app
    with open('subjectDatabase.json','w', encoding='utf-8') as f:
        json.dump(data,f)


''' Check in console if the subjects are well extracted, and then write them in the database '''
year, first_semester, second_semester, subjects_first_semester, subjects_second_semester, specialite = getSubjectsFromHTML('APP3_INFO_23-24.html')

print('\nAnnée :',year,'\n\n')
print('Spécialité :',specialite,'\n\n')
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

''' Write them in the database '''
# formCategoriesPEIP(year, first_semester, second_semester, subjects_first_semester, subjects_second_semester)
formCategoriesAPP3(year, first_semester, second_semester, subjects_first_semester, subjects_second_semester, specialite)
# addSpecialiteAPP(first_semester, second_semester, specialite)