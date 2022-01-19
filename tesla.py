import requests
from pprint import pprint

def getInternships():  # sourcery skip: inline-immediately-returned-variable
    url = "https://www.tesla.com/cua-api/apps/careers/state"
    r = requests.get(url).json()

    # regions = r['lookup']['regions']
    # countries = r['lookup']['countries']
    # locations = r['lookup']['locations']
    # departments = r['lookup']['departments']
    # types = r['lookup']['types']

    locationsFR = [element for sublist in [e for e in [e for e in r['geo'] if e['id'] == "3"][0]
                                           ['countries'] if e['id'] == "FR"][0]['cities'].values() for element in sublist]

    listings = r['listings']

    internships = [
        listing
        for listing in listings
        # select only internships in France
        if listing['y'] == 3 and listing['l'] in locationsFR
    ]

    return internships

def getInternshipInfos(id):
    return requests.get(
        f'https://www.tesla.com/cua-api/careers/job/{id}').json()

if __name__ == '__main__':
    for internship in getInternships():
        pprint(getInternshipInfos(internship['id']))
