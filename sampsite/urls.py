"""sampsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

# url matches the URL in the browser to a module
# in your Django project
from django.conf.urls import url

# Loads URLs for Admin site
from django.contrib import admin

# Reference my hello_world function
from sampsite.views import hello_world, root_page, random_number

# 3 include allows you to reference other url files
# in our project
from django.conf.urls import include

# Lists all URLs
# Add the directory in the URL you want tied to
# the hello_world function
# The r means we want to treat this like a raw string
# that ignored backslashes
# Then we define a regular expression where ^ is the
# beginning of a string, then we have the text to match
# The $ signifies the end of a Regex string

# We can pass data to a function by surrounding the part
# of the Regex to send with parentheses
# If they didn't enter a number I provide a default max
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^helloworld/$', hello_world),
    url(r'^$', root_page),
    url(r'^random/(\d+)/$', random_number),
    url(r'^random/$', random_number),

    # 3 Reference the root of the polls app
    url(r'^flights/', include('flights.urls')),
]

# 3 Test that the polls URL works by running the server
# python3 manage.py runserver
# Go to localhost:8000/polls/

# 3 Setup the database in settings.py
