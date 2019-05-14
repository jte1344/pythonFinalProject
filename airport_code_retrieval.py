'''
This function takes a city name and returns the airport code from the IATA airport codes api
'''

import requests
import json


def airport_code(city):

    # Set apiKey
    apiKey = 'a4f285e4-5b80-4d82-b32a-725173d2be04'

    # Set url
    url = 'https://iatacodes.org/api/v6/autocomplete?api_key={}&query={}'.format(apiKey, city)

    # Set agent
    userAgent = "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11"
    headers = {'User-Agent': userAgent}
    results = requests.get(url, headers=headers, verify=False)
    results.raise_for_status()

    # convert city data to a dictionary to be read
    codeDict = json.loads(results.text)

    # This allows the user to search using a city name or a specific airport name
    try:
        code = codeDict['response']['airports_by_cities'][0]['code']
    except IndexError:
        code = codeDict['response']['airports'][0]['code']


    return code


# Test the code
print(airport_code('denver'))
