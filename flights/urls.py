from django.conf.urls import url

from . import views

# 2 Add a reference to the view and assign it to
# the root URL for polls

app_name = 'flights'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^hotels$', views.hotels, name='hotels'),
    url(r'^rentals$', views.rentals, name='rentals'),
]
