init:

  run:

  pip install django-widget-tweaks

  (and make sure django is installed)

  most imports that are used (so make sure you have them installed and can use them correctly):

  import json
  import os,sys
  import requests
  import requests,re
  from django import forms
  from django.http import HttpResponse
  from django.http import HttpResponseRedirect
  from django.shortcuts import render, redirect
  from django.shortcuts import get_object_or_404
  from django.urls import reverse
  from collections import OrderedDict
  from datetime import datetime
  from time import time
  from lxml import html,etree



1) cd to the root directory (contains manage.py)

2) run:

    python manage.py runserver

    if any errors one or more modules may not be installed...

3)

    go to http://localhost:8000/flights/
