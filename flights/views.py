# 1 Create the polls app inside our project
# 1 python3 manage.py startapp polls
# 1 You can have multiple apps in your project
# 1 Now we will create a view

from django.http import HttpResponse
from django.shortcuts import render
from .models import Question, Choice
from django.shortcuts import get_object_or_404

def index(request):
    #latest
    context = {'hero': 1}
    return render(request, 'flights/index.html', context)

def detail(request, question_id):
    return HttpResponse("You're looking at question %s" % question_id)

def results(request, question_id):
    return HttpResponse("You're looking at the results of question %s" % question_id)

# 1 Now attach the view to a url in urls.py
