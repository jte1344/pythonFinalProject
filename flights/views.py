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
from collections import OrderedDict
from datetime import datetime
from time import time
from lxml import html,etree
import requests,re
import os,sys


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

                outBound = parseHotel(location, dateFrom, dateTo, 'popularity')

                data = {'location': location, 'dateTo': dateTo, 'dateFrom': dateFrom}

                try:
                    clip = getCityUrl(location)
                except:
                    clip = "https://d1ic4altzx8ueg.cloudfront.net/finder-au/wp-uploads/2016/05/Airplane.Square.jpg"


                print(outBound)

                return render(request, 'flights/yourHotel.html', {'outBound': outBound, 'clip': clip, 'data': data})

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




'''def parseHotel(location, start, end):

    start = start.replace("/", "-")
    end = end.replace("/", "-")

    url = "https://www.hotels.com/search/search.html?resolved-location=CITY%3A1516192%3AUNKNOWN%3AUNKNOWN&destination-id=1516192&q-destination={0}&q-check-in={1}&q-check-out={2}&q-rooms=1&q-room-0-adults=2&q-room-0-children=0".format(location, start, end)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}

    response = requests.get(url, headers=headers)
'''



def parseHotel(locality,checkin_date,checkout_date,sort):


    checkIn = checkin_date
    checkOut = checkout_date
    print("Scraper Inititated for Locality:%s"%locality)
    # TA rendering the autocomplete list using this API
    print("Finding search result page URL")
    geo_url = 'https://www.tripadvisor.com/TypeAheadJson?action=API&startTime='+str(int(time()))+'&uiOrigin=GEOSCOPE&source=GEOSCOPE&interleaved=true&types=geo,theme_park&neighborhood_geos=true&link_type=hotel&details=true&max=12&injectNeighborhoods=true&query='+locality
    api_response  = requests.get(geo_url, verify=False).json()
    #getting the TA url for th equery from the autocomplete response
    url_from_autocomplete = "http://www.tripadvisor.com"+api_response['results'][0]['url']
    print('URL found %s'%url_from_autocomplete)
    geo = api_response['results'][0]['value']
    #Formating date for writing to file

    date = checkin_date+"_"+checkout_date
    #form data to get the hotels list from TA for the selected date
    form_data = {'changeSet': 'TRAVEL_INFO',
            'showSnippets': 'false',
            'staydates':date,
            'uguests': '2',
            'sortOrder':sort
    }
    #Referrer is necessary to get the correct response from TA if not provided they will redirect to home page
    headers = {
                            'Accept': 'text/javascript, text/html, application/xml, text/xml, */*',
                            'Accept-Encoding': 'gzip,deflate',
                            'Accept-Language': 'en-US,en;q=0.5',
                            'Cache-Control': 'no-cache',
                            'Connection': 'keep-alive',
                            'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
                            'Host': 'www.tripadvisor.com',
                            'Pragma': 'no-cache',
                            'Referer': url_from_autocomplete,
                            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:28.0) Gecko/20100101 Firefox/28.0',
                            'X-Requested-With': 'XMLHttpRequest'
                        }
    cookies=  {"SetCurrency":"USD"}
    print("Downloading search results page")
    page_response  = requests.post(url = url_from_autocomplete,data=form_data,headers = headers, cookies = cookies, verify=False)
    print("Parsing results ")
    parser = html.fromstring(page_response.text)
    hotel_lists = parser.xpath('//div[contains(@class,"listItem")]//div[contains(@class,"listing collapsed")]')
    hotel_data = []
    if not hotel_lists:
        hotel_lists = parser.xpath('//div[contains(@class,"listItem")]//div[@class="listing "]')

    for hotel in hotel_lists:
        XPATH_HOTEL_LINK = './/a[contains(@class,"property_title")]/@href'
        XPATH_REVIEWS  = './/a[@class="review_count"]//text()'
        XPATH_RANK = './/div[@class="popRanking"]//text()'
        XPATH_RATING = './/span[contains(@class,"rating")]/@alt'
        XPATH_HOTEL_NAME = './/a[contains(@class,"property_title")]//text()'
        XPATH_HOTEL_FEATURES = './/div[contains(@class,"common_hotel_icons_list")]//li//text()'
        XPATH_HOTEL_PRICE = './/div[contains(@data-sizegroup,"mini-meta-price")]/text()'
        XPATH_VIEW_DEALS = './/div[contains(@data-ajax-preserve,"viewDeals")]//text()'
        XPATH_BOOKING_PROVIDER = './/div[contains(@data-sizegroup,"mini-meta-provider")]//text()'

        raw_booking_provider = hotel.xpath(XPATH_BOOKING_PROVIDER)
        raw_no_of_deals =  hotel.xpath(XPATH_VIEW_DEALS)
        raw_hotel_link = hotel.xpath(XPATH_HOTEL_LINK)
        raw_no_of_reviews = hotel.xpath(XPATH_REVIEWS)
        raw_rank = hotel.xpath(XPATH_RANK)
        raw_rating = hotel.xpath(XPATH_RATING)
        raw_hotel_name = hotel.xpath(XPATH_HOTEL_NAME)
        raw_hotel_features = hotel.xpath(XPATH_HOTEL_FEATURES)
        raw_hotel_price_per_night  = hotel.xpath(XPATH_HOTEL_PRICE)

        url = 'http://www.tripadvisor.com'+raw_hotel_link[0] if raw_hotel_link else  None
        reviews = ''.join(raw_no_of_reviews).replace("reviews","").replace(",","") if raw_no_of_reviews else 0
        rank = ''.join(raw_rank) if raw_rank else None
        rating = ''.join(raw_rating).replace('of 5 bubbles','').strip() if raw_rating else None
        name = ''.join(raw_hotel_name).strip() if raw_hotel_name else None
        hotel_features = ','.join(raw_hotel_features)
        price_per_night = ''.join(raw_hotel_price_per_night).replace('\n','') if raw_hotel_price_per_night else None
        no_of_deals = re.findall("all\s+?(\d+)\s+?",''.join(raw_no_of_deals))
        booking_provider = ''.join(raw_booking_provider).strip() if raw_booking_provider else None

        if no_of_deals:
            no_of_deals = no_of_deals[0]
        else:
            no_of_deals = 0

        data = {
                    'hotel_name':name,
                    'url':url,
                    'locality':locality,
                    'reviews':reviews,
                    'tripadvisor_rating':rating,
                    'checkOut':checkOut,
                    'checkIn':checkIn,
                    'hotel_features':hotel_features,
                    'price_per_night':price_per_night,
                    'no_of_deals':no_of_deals,
                    'booking_provider':booking_provider

        }
        hotel_data.append(data)
    return hotel_data
