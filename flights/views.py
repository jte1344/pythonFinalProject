# 1 Create the polls app inside our project
# 1 python3 manage.py startapp polls
# 1 You can have multiple apps in your project
# 1 Now we will create a view

from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Question, Choice
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import ContactForm, ContactFormHotel, ContactFormRental
import json
import requests
from lxml import html
from collections import OrderedDict



def index(request):

    if request.method == 'POST':
        form = ContactForm(request.POST)

        if form.is_valid():

            locFrom = request.POST["locFrom"]#source
            locTo = request.POST["locTo"]#destination
            dateFrom = request.POST["dateFrom"]#date leaving
            dateTo = request.POST["dateTo"]#date returning

            outBound = parse(locFrom, locTo, dateFrom)


            try:
                clip = getCityUrl(outBound[0]['arrival'])
            except:
                clip = "https://d1ic4altzx8ueg.cloudfront.net/finder-au/wp-uploads/2016/05/Airplane.Square.jpg"


            data = {'locTo': locTo, 'locFrom': locFrom, 'dateTo': dateTo, 'dateFrom': dateFrom}

            return render(request, 'flights/yourFlight.html', {'outBound': outBound, 'clip': clip, 'data': data})

    else:
        form = ContactForm()
        return render(request, 'flights/index.html', {'form': form})



def hotels(request):

        if request.method == 'POST':
            form = ContactFormHotel(request.POST)

            if form.is_valid():

                location = request.POST["location"]
                dateFrom = request.POST["dateFrom"]
                dateTo = request.POST["dateTo"]

                data = {'location': location, 'dateTo': dateTo, 'dateFrom': dateFrom}



                return render(request, 'flights/yourHotel.html', data)

        else:
            form = ContactFormHotel()
            return render(request, 'flights/hotels.html', {'form': form})



def rentals(request):

            if request.method == 'POST':
                form = ContactFormRental(request.POST)

                if form.is_valid():

                    location = request.POST["location"]
                    dateFrom = request.POST["dateFrom"]
                    dateTo = request.POST["dateTo"]

                    data = {'location': location, 'dateTo': dateTo, 'dateFrom': dateFrom}

                    return render(request, 'flights/yourRental.html', data)

            else:
                form = ContactFormRental()
                return render(request, 'flights/rentals.html', {'form': form})









def parse(source, destination, date):
    for i in range(5):

        try:

            # The url uses positional argument definitions to adjust the search pattern appropriately
            # This may work for other sites and we can skip the traversing of pages entirely.
            url = "https://www.expedia.com/Flights-Search?trip=oneway&leg1=from:{0},to:{1},departure:{2}TANYT&passengers=adults:1,children:0,seniors:0,infantinlap:Y&options=cabinclass%3Aeconomy&mode=search&origref=www.expedia.com".format(
                source, destination, date)

            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}

            response = requests.get(url, headers=headers)

            parser = html.fromstring(response.text)

            json_data_xpath = parser.xpath("//script[@id='cachedResultsJson']//text()")

            raw_json = json.loads(json_data_xpath[0] if json_data_xpath else '')

            flight_data = json.loads(raw_json["content"])

            flight_info = OrderedDict()

            lists = []

            for i in flight_data['legs'].keys():

                total_distance = flight_data['legs'][i].get("formattedDistance", '')

                exact_price = flight_data['legs'][i].get('price', {}).get('totalPriceAsDecimal', '')

                departure_location_airport = flight_data['legs'][i].get('departureLocation', {}).get('airportLongName',
                                                                                                     '')

                departure_location_city = flight_data['legs'][i].get('departureLocation', {}).get('airportCity', '')

                departure_location_airport_code = flight_data['legs'][i].get('departureLocation', {}).get('airportCode',
                                                                                                          '')

                arrival_location_airport = flight_data['legs'][i].get('arrivalLocation', {}).get('airportLongName', '')

                arrival_location_airport_code = flight_data['legs'][i].get('arrivalLocation', {}).get('airportCode', '')

                arrival_location_city = flight_data['legs'][i].get('arrivalLocation', {}).get('airportCity', '')

                airline_name = flight_data['legs'][i].get('carrierSummary', {}).get('airlineName', '')

                no_of_stops = flight_data['legs'][i].get("stops", "")

                flight_duration = flight_data['legs'][i].get('duration', {})

                flight_hour = flight_duration.get('hours', '')

                flight_minutes = flight_duration.get('minutes', '')

                flight_days = flight_duration.get('numOfDays', '')

                if no_of_stops == 0:

                    stop = "Nonstop"

                else:

                    stop = str(no_of_stops) + ' Stop'

                total_flight_duration = "{0} days {1} hours {2} minutes".format(flight_days, flight_hour,
                                                                                flight_minutes)

                departure = departure_location_airport + departure_location_city

                arrival = arrival_location_airport + arrival_location_city

                carrier = flight_data['legs'][i].get('timeline', [])[0].get('carrier', {})

                plane = carrier.get('plane', '')

                plane_code = carrier.get('planeCode', '')

                formatted_price = "{0:.2f}".format(exact_price)

                if not airline_name:
                    airline_name = carrier.get('operatedBy', '')

                timings = []

                for timeline in flight_data['legs'][i].get('timeline', {}):

                    if 'departureAirport' in timeline.keys():
                        departure_airport = timeline['departureAirport'].get('longName', '')

                        departure_time = timeline['departureTime'].get('time', '')

                        arrival_airport = timeline.get('arrivalAirport', {}).get('longName', '')

                        arrival_time = timeline.get('arrivalTime', {}).get('time', '')

                        flight_timing = {

                            'departure_airport': departure_airport,

                            'departure_time': departure_time,

                            'arrival_airport': arrival_airport,

                            'arrival_time': arrival_time

                        }

                        timings.append(flight_timing)

                flight_info = {'stops': stop,

                               'ticket_price': formatted_price,

                               'departure': departure,

                               'arrival': arrival,

                               'flight duration': total_flight_duration,

                               'airline': airline_name,

                               'plane': plane,

                               'timings': timings,

                               'plane code': plane_code

                               }

                lists.append(flight_info)

            sortedlist = sorted(lists, key=lambda k: k['ticket_price'], reverse=False)

            return sortedlist

        except ValueError:

            print("Retrying...")

        return {"error": "failed to process the page", }




def getCityUrl(city):

    #replces any spaces with a dash (for correct URL)
    city = city.lower()
    city = city.replace(" ", "-")
    print(city)
    #gets the json from the created URL
    url1 ='https://api.teleport.org/api/urban_areas/slug:' + city + '/images'
    res1 = requests.get(url1)
    res1.raise_for_status()#handles error at 404s
    locationData = json.loads(res1.text)

    return locationData["photos"][0]["image"]["web"]
