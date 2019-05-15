# 1 Create the polls app inside our project
# 1 python3 manage.py startapp polls
# 1 You can have multiple apps in your project
# 1 Now we will create a view

from django.http import HttpResponse
from django.shortcuts import render, redirect
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
            inBound = parse(locTo, locFrom, dateTo)



            print(outBound)

            try:
                clip = getCityUrl(outBound[0]['arrival'])
            except:
                clip = "https://d1ic4altzx8ueg.cloudfront.net/finder-au/wp-uploads/2016/05/Airplane.Square.jpg"


            data = {'locTo': locTo, 'locFrom': locFrom, 'dateTo': dateTo, 'dateFrom': dateFrom}

            return render(request, 'flights/yourFlight.html', {'outBound': outBound, 'inBound': inBound, 'clip': clip, 'data': data})

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


                return render(request, 'flights/yourHotel.html', {'outBound': outBound, 'clip': clip, 'data': data})

        else:
            form = ContactFormHotel()
            return render(request, 'flights/hotels.html', {'form': form})



def rentals(request):

            if request.method == 'POST':
                form = ContactFormRental(request.POST)

                if form.is_valid():

                    location = request.POST["location"].lower()
                    state = request.POST["state"].upper()
                    dateFrom = request.POST["dateFrom"]
                    dateTo = request.POST["dateTo"]

                    rentalDate = dateFrom[6:10] + dateFrom[0:2] + dateFrom[3:5]
                    returnDate = dateTo[6:10] + dateTo[0:2] + dateTo[3:5]

                    url = "https://www.priceline.com/drive/search/r/{0},%20{1}/{0},%20{1}/{2}-12:00/{3}-12:00/list?paidSearchCode=DEFAULT&query=discount%20rental%20cars&lp=y&kw=discount%20rental%20cars&match=b&adp=1t1&refid=PLGOOGLECPC&refclickid=D%3AcRental-Car14486525080g3109529648921014450214kwd-23895126%7C9028803%7C1t1&gclid=CjwKCAjwiN_mBRBBEiwA9N-e_l-IllR0qSOCKX3wJeWCoS1mC2fz3u03bqze-HiDJEriSZCFiXXcHxoCaX4QAvD_BwE&slingshot=1702".format(location, state, rentalDate, returnDate)

                    data = {'location': location, 'dateTo': dateTo, 'dateFrom': dateFrom}

                    return redirect(url)

            else:
                form = ContactFormRental()
                return render(request, 'flights/rentals.html', {'form': form})









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

                departure = departure_location_airport + departure_location_city

                arrival = arrival_location_airport + arrival_location_city

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

                               'ticket_price': formatted_price,

                               'departure_date': date,

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
            sorted_list = sorted(lists, key=lambda k: k['ticket_price'], reverse=False)

            # reduce the list to the cheapest 3 flights
            cut_list = sorted_list[:6]

            # return the reduced list
            return cut_list

        # catch if the scrap fails at some point
        except ValueError:

            print("Retrying...")

    return {"error": "failed to process the page", }



def date_range_creator(date):

    # Initialize return value
    dateRange = []

    # create date regex
    dateRegex = re.compile(r'([01][0-9])/([0-3][0-9])/([0-9]{4})')
    mo = dateRegex.search(date)

    # Strip each section of the date for use in datetime
    month = int(mo[1])
    day = int(mo[2])
    year = int(mo[3])

    # Create initial date datetime
    initialDate = datetime.date(month=month, day=day, year=year)

    # Incriment the initial date to two new dates
    firstNewDate = initialDate + datetime.timedelta(days=1)
    secondNewDate = initialDate + datetime.timedelta(days=2)

    # Adjust formatting of the new dates
    firstNewDate = firstNewDate.strftime("%m/%d/%Y")
    secondNewDate = secondNewDate.strftime("%m/%d/%Y")

    # Add all dates to the range list
    dateRange.append(date)
    dateRange.append(firstNewDate)
    dateRange.append(secondNewDate)

    return dateRange


def getCityUrl(city):

    #replces any spaces with a dash (for correct URL)
    city = city.lower()

    city = city.replace(" ", "-")

    #gets the json from the created URL
    url1 ='https://api.teleport.org/api/urban_areas/slug:' + city + '/images'

    res1 = requests.get(url1)

    res1.raise_for_status()#handles error at 404s

    locationData = json.loads(res1.text)

    return locationData["photos"][0]["image"]["web"]






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

        rank = './/div[@class="popRanking"]//text()'

        rating = './/span[contains(@class,"rating")]/@alt'

        reviews  = './/a[@class="review_count"]//text()'

        hotelLink = './/a[contains(@class,"property_title")]/@href'

        hotelName = './/a[contains(@class,"property_title")]//text()'

        deals = './/div[contains(@data-ajax-preserve,"viewDeals")]//text()'

        features = './/div[contains(@class,"common_hotel_icons_list")]//li//text()'

        provider = './/div[contains(@data-sizegroup,"mini-meta-provider")]//text()'

        price = './/div[contains(@data-sizegroup,"mini-meta-price")]/text()'






        raw_rank = hotel.xpath(rank)

        raw_rating = hotel.xpath(rating)

        raw_no_of_reviews = hotel.xpath(reviews)

        raw_hotel_link = hotel.xpath(hotelLink)

        raw_hotel_name = hotel.xpath(hotelName)

        raw_no_of_deals =  hotel.xpath(deals)

        raw_hotel_features = hotel.xpath(features)

        raw_booking_provider = hotel.xpath(provider)

        raw_hotel_price_per_night  = hotel.xpath(price)





        url = 'http://www.tripadvisor.com'+raw_hotel_link[0] if raw_hotel_link else None

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
