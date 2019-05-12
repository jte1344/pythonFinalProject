'''
This will take the same departure and destination data, as well as the range of dates to leave and return.
It will use them to loop through the dates and call the scrappers for each direction of flight for each of the days.
It currently only calls the tutorial_test parser, but it should work with any scrapper, provided we adjust the output.
'''

from tutorial_test import parse
import json


def date_loop(origin, destination, depart_dates, ret_dates):

    # Find departure flights
    for date in depart_dates:

        print("Fetching flight details")

        # We can add the other scrappers to this so it gets all of the json data from each site
        scraped_data = parse(origin, destination, date)

        print("Writing data to output file")

        # The date format that works for the scrapper does not work for the file writer
        date = date.replace('/', '-')

        # right now this just creates files for the tester scrapper, but we can change this as needed
        with open('%s-%s-%s-flight-results.json' % (origin, destination, date), 'w') as fp:
            json.dump(scraped_data, fp, indent=4)

    # Find return flights
    for date in ret_dates:

        print("Fetching flight details")

        # We can add the other scrappers to this so it gets all of the json data from each site
        scraped_data = parse(destination, origin, date)

        print("Writing data to output file")

        # The date format that works for the scrapper does not work for the file writer
        date = date.replace('/', '-')

        # right now this just creates files for the tester scrapper, but we can change this as needed
        with open('%s-%s-%s-flight-results.json' % (destination, origin, date), 'w') as fp:
            json.dump(scraped_data, fp, indent=4)


# testing dates
depart = ['06/05/2019', '06/06/2019', '06/07/2019']
ret = ['06/12/2019', '06/13/2019', '06/14/2019']

# test call
date_loop('den', 'ord', depart, ret)
