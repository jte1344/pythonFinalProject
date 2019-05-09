from django.conf.urls import url

from . import views

# 2 Add a reference to the view and assign it to
# the root URL for polls

app_name = 'flights'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<question_id>[0-9]+)$', views.detail, name='detail'),
    url(r'^(?P<question_id>[0-9]+)/results/$', views.results, name='index'),
]
