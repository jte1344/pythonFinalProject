'''
This scraper will be called from the dates loop for each date for the trip.
It uses lxml-html to parse the page and populates the needed flight information into a list for each flight on that day.
It then adds each flight for the day to a list of dictionaries, before sorting them by price and then cutting the list
to only return the three cheapest flights for the day.
'''

# import needed modules
import json
import requests
from lxml import html


# define the parsing function for expedia
def parse(source, destination, date):

    # Let the parse try to run 5 times before exiting as failed
    for i in range(5):

        # Start block to attempt scrape
        try:

            # Set the url for calling the scrape
            url = "https://www.expedia.com/Flights-Search?trip=oneway&leg1=from:{0},to:{1},departure:{2}TANYT&passengers=adults:1,children:0,seniors:0,infantinlap:Y&options=cabinclass%3Aeconomy&mode=search&origref=www.expedia.com".format(
                source, destination, date)

            # set the headers
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}

            # get the page to scrape
            response = requests.get(url, headers=headers)

            # parse the page
            parser = html.fromstring(response.text)

            # get the data in json format
            json_data_xpath = parser.xpath("//script[@id='cachedResultsJson']//text()")
            raw_json = json.loads(json_data_xpath[0] if json_data_xpath else '')
            flight_data = json.loads(raw_json["content"])

            # initialize the lists to return
            lists = []

            # get info for each leg of the flight
            for i in flight_data['legs'].keys():

                # Each piece has a descriptive name to tell what info is being obtained
                exact_price = flight_data['legs'][i].get('price', {}).get('totalPriceAsDecimal', '')

                departure_location_airport = flight_data['legs'][i].get('departureLocation', {}).get('airportLongName',
                                                                                                     '')
                departure_location_city = flight_data['legs'][i].get('departureLocation', {}).get('airportCity', '')

                arrival_location_airport = flight_data['legs'][i].get('arrivalLocation', {}).get('airportLongName', '')

                arrival_location_city = flight_data['legs'][i].get('arrivalLocation', {}).get('airportCity', '')

                airline_name = flight_data['legs'][i].get('carrierSummary', {}).get('airlineName', '')

                no_of_stops = flight_data['legs'][i].get("stops", "")

                flight_duration = flight_data['legs'][i].get('duration', {})

                flight_hour = flight_duration.get('hours', '')

                flight_minutes = flight_duration.get('minutes', '')

                flight_days = flight_duration.get('numOfDays', '')

                # Set how many stops are in the flight, this can vary so needs the if/else block
                if no_of_stops == 0:

                    # Non-stop flight
                    stop = "Nonstop"

                else:

                    # at least one stop in the flight
                    stop = str(no_of_stops) + ' Stop'

                # continue descriptive information scrape
                total_flight_duration = "{0} days {1} hours {2} minutes".format(flight_days, flight_hour, flight_minutes)

                departure = departure_location_airport + ", " + departure_location_city

                arrival = arrival_location_airport + ", " + arrival_location_city

                carrier = flight_data['legs'][i].get('timeline', [])[0].get('carrier', {})

                plane = carrier.get('plane', '')

                plane_code = carrier.get('planeCode', '')

                # format the price to a float value with 2 decimals
                formatted_price = "{0:.2f}".format(exact_price)

                # set airline name only if it hasn't already been set
                if not airline_name:
                    airline_name = carrier.get('operatedBy', '')

                # Initialize the timeline list for the dict
                timings = []

                # Get details on the timeline for the flight
                for timeline in flight_data['legs'][i].get('timeline', {}):

                    # ensure the departure airport is in the keys
                    if 'departureAirport' in timeline.keys():

                        # set flight timing details to info from the scrape
                        departure_airport = timeline['departureAirport'].get('longName', '')

                        departure_time = timeline['departureTime'].get('time', '')

                        arrival_airport = timeline.get('arrivalAirport', {}).get('longName', '')

                        arrival_time = timeline.get('arrivalTime', {}).get('time', '')

                        # populate the flight timings dictionary
                        flight_timing = {

                            'departure_airport': departure_airport,

                            'departure_time': departure_time,

                            'arrival_airport': arrival_airport,

                            'arrival_time': arrival_time

                        }

                        # add the timings details to the timings list
                        timings.append(flight_timing)

                # populate the flight information dictionary
                flight_info = {'stops': stop,

                               'ticket price': formatted_price,

                               'departure date': date,

                               'departure': departure,

                               'arrival': arrival,

                               'flight duration': total_flight_duration,

                               'airline': airline_name,

                               'plane': plane,

                               'timings': timings,

                               'plane code': plane_code

                               }

                # add the flight details to the list
                lists.append(flight_info)

            # Sort the list by price
            sorted_list = sorted(lists, key=lambda k: k['ticket price'], reverse=False)

            # reduce the list to the cheapest 3 flights
            cut_list = sorted_list[:3]

            # return the reduced list
            return cut_list

        # catch if the scrap fails at some point
        except ValueError:

            print("Retrying...")

    return {"error": "failed to process the page", }
