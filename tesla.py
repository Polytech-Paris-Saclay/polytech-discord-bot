import requests
from pprint import pprint

url = "https://www.tesla.com/cua-api/apps/careers/state"
r = requests.get(url)
data = r.json()

# get all locations in a country
def getLocations(_country='FR', _region='3'):
    # regions = data['lookup']['regions']
    # countries = data['lookup']['countries']
    # locations = data['lookup']['locations']
    # departments = data['lookup']['departments']
    # types = data['lookup']['types']

    locations = []

    # select only the specified region
    for region in data['geo']:
        if region['id'] == _region:

            # select only the specified country
            for country in region['sites']:
                if country['id'] == _country:

                    # get all the locations in the specified country
                    for city in country['cities'].values():
                        for location in city:
                            locations.append(location)

    return locations

# get all internships in a country


def getInternships(_country='FR', _region='3'):
    locations = getLocations(_country, _region)

    listings = data['listings']

    internships = [
        listing
        for listing in listings
        # select only internships in France
        if listing['y'] == 3 and listing['l'] in locations
    ]

    return internships

def getInternshipInfos(id):
    return requests.get(
        f'https://www.tesla.com/cua-api/careers/job/{id}').json()


if __name__ == '__main__':
    country = 'FR'
    region = '3'
    internships = getInternships(country, region)

    if len(internships):
        for internship in internships:
            pprint(getInternshipInfos(internship['id']))
    else:
        print('No new internships')
