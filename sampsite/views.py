from django.http import HttpResponse

import random

# This is our View function which receives info
# on the request
def hello_world(request):

    # Return a response object with the text Hello World
    return HttpResponse("Hello World")

def root_page(request):

    return HttpResponse("Root Home Page")

# Receives the number passed in the url and then returns
# a random number
def random_number(request, max_rand=100):

    # Calculate a random number between 0 and the number passed
    random_num = random.randrange(0, int(max_rand))

    # Place the string and decimal in the output
    msg = "Random Number Between 0 and %s : %d" % (max_rand, random_num)

    return HttpResponse(msg)
 
