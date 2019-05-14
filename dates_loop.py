'''
This will take the same departure and destination data, as well as the range of dates to leave and return.
It will use them to loop through the dates and call the scrappers for each direction of flight for each of the days.
It currently only calls the tutorial_test parser, but it should work with any scrapper, provided we adjust the output.
'''

from expedia_scrapper import parse
from date_adjuster import date_range_creator
from airport_code_retrieval import airport_code
#import pprint


def date_loop(origin, destination, depart_date, ret_date):

    # Initialize data structure to return
    flightList = []
    
    # Get origin and destination airport codes
    originCode = airport_code(origin)
    destinationCode = airport_code(destination)

    # generate range of dates to scrap
    depart_dates = date_range_creator(depart_date)
    ret_dates = date_range_creator(ret_date)

    # Find departure flights
    for date in depart_dates:

        print("Fetching flight details")

        # We can add the other scrappers to this so it gets all of the json data from each site
        scraped_data = parse(originCode, destinationCode, date)

        print("Updating Flight Dictionary")

        # Add flight to the dictionary
        flightList.append(scraped_data)


    # Find return flights
    for date in ret_dates:

        print("Fetching flight details")

        # We can add the other scrappers to this so it gets all of the json data from each site
        scraped_data = parse(destinationCode, originCode, date)

        print("Updating Flight Dictionary")

        # Add flight to the dictionary
        flightList.append(scraped_data)

    return flightList


# testing dates
depart = '06/05/2019'
ret = '06/12/2019'

# test call
pprint.pprint(date_loop('den', 'ord', depart, ret))
