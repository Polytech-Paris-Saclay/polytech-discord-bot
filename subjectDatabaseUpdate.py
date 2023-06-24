import json
from oasis import getSubjects
from getSubjectsWithHTML import getSubjectsFromHTML

def formCategories(first_semester, second_semester, subjects_first_semester, subjects_second_semester):
    '''first_semester'''
    first_semester_name = 'S' + str(first_semester)
    # tronc commun : UE 2 et 3 + UE1 except anglais
    tronc_commun = []
    tronc_commun.extend(subjects_first_semester[2])
    tronc_commun.extend(subjects_first_semester[1])
    tronc_commun.extend(subjects_first_semester[0][1:]) if len(subjects_first_semester[0][1:]) > 1 else None 
    # options : UE 4 except 3 last subjects
    options = []
    options.extend(subjects_first_semester[3][:-3])
    # parcours : last 3 subjects of UE 4
    parcours = []
    parcours.extend(subjects_first_semester[3][-3:])
    
    globals()[first_semester_name] = {
        'tronc_commun': tronc_commun,
        'options': options,
        'parcours': parcours
    }
    '''second_semester'''
    second_semester_name = 'S' + str(second_semester)
    # tronc commun : UE 2 et 3 + UE1 except anglais
    tronc_commun = []
    tronc_commun.extend(subjects_second_semester[2])
    tronc_commun.extend(subjects_second_semester[1])
    tronc_commun.extend(subjects_first_semester[0][1:]) if len(subjects_first_semester[0][1:]) > 1 else None
    # options : UE 4 except 3 last subjects
    options = []
    options.extend(subjects_second_semester[3][:-3])
    # parcours : last 3 subjects of UE 4
    parcours = []
    parcours.extend(subjects_first_semester[3][-3:])
    globals()[second_semester_name] = {
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

''' Check in console if the subjects are well extracted, and then write them in the database '''
year, first_semester, second_semester, subjects_first_semester, subjects_second_semester = getSubjectsFromHTML('mychoices.html')

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

''' Write them in the database '''
formCategories(first_semester, second_semester, subjects_first_semester, subjects_second_semester)