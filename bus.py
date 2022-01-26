import requests
from pprint import pprint

stations = {
    687639239: 'Gare de Massy Palaiseau',
    687639261: 'Université Paris-Saclay',
    687639310: 'Orly 1,2,3',
}

def getNextBuses(station = 687639261):
    headers = { "X-Requested-With" : "XMLHttpRequest" }
    r = requests.get(f'https://www.transdev-idf.com/ajax/station/{station}/nextbus', headers=headers)
    return r.json()

if __name__ == '__main__':
    pprint(getNextBuses())
