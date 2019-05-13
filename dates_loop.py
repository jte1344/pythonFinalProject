'''
This will take the same departure and destination data, as well as the range of dates to leave and return.
It will use them to loop through the dates and call the scrappers for each direction of flight for each of the days.
It currently only calls the tutorial_test parser, but it should work with any scrapper, provided we adjust the output.
'''

from expedia_scrapper import parse
import pprint


def date_loop(origin, destination, depart_dates, ret_dates):

    # Initialize data structure to return
    flightList = []

    # Find departure flights
    for date in depart_dates:

        print("Fetching flight details")

        # We can add the other scrappers to this so it gets all of the json data from each site
        scraped_data = parse(origin, destination, date)

        print("Updating Flight Dictionary")

        # Add flight to the dictionary
        flightList.append(scraped_data)


    # Find return flights
    for date in ret_dates:

        print("Fetching flight details")

        # We can add the other scrappers to this so it gets all of the json data from each site
        scraped_data = parse(destination, origin, date)

        print("Updating Flight Dictionary")

        # Add flight to the dictionary
        flightList.append(scraped_data)

    return flightList


# testing dates
depart = ['06/05/2019', '06/06/2019', '06/07/2019']
ret = ['06/12/2019', '06/13/2019', '06/14/2019']

# test call
pprint.pprint(date_loop('den', 'ord', depart, ret))
