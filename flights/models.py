# 5 Here you define the names and data types for
# 5 the information you are storing in your database

from django.db import models

import datetime
from django.utils import timezone

# 5 Create your models here.
# 5 Each model is a class with class variables that
# 5 represent fields in your database
# 5 After setting the column names an data types the DB
# 5 can create the table

class Question(models.Model):

    # 5 Define a DB column called question_text which
    # 5 contains text with a max size of 200
    question_text = models.CharField(max_length=200)

    # 5 This contains a date and the text passed is an
    # 5 optional human readable name
    pub_date = models.DateTimeField('date published')

    # 7 Return the text for the question when the Question
    # 7 is called by editing __str__

    def __str__(self):
        return self.question_text

    # 7 Here is a custom method for returning whether
    # 7 the question was published recently
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

class Choice(models.Model):

    # 5 Define that each choice is related to a single
    # 5 Question
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    # 7 Return the Choice text as well
    def __str__(self):
        return self.choice_text

    # 7 Let's test our changes : python3 manage.py shell
    # 7 from polls.models import Question, Choice
    # 7 Get a detailed list of questions
    # 7 Question.objects.all()

    # 7 Get the Question with the matching id
    # 7 Question.objects.filter(id=1)

    # 7 Get the question that starts with What
    # 7 Question.objects.filter(question_text__startswith='What')

    # 7 Get Question published this year
    # 7 from django.utils import timezone
    # 7 current_year = timezone.now().year
    # 7 Question.objects.get(pub_date__year=current_year)

    # 7 If you request something that doesn't exist you
    # 7 raise an exception
    # 7 Question.objects.get(id=2)

    # 7 Search for primary key
    # 7 Question.objects.get(pk=1)

    # 7 Test was_published_recently()
    # 7 q = Question.objects.get(pk=1)
    # 7 q.was_published_recently()

    # 7 Show choices for matching question
    # 7 q.choice_set.all()

    # 7 Add new choices
    # 7 q.choice_set.create(choice_text='Not Much', votes=0)
    # 7 q.choice_set.create(choice_text='The Sky', votes=0)
    # 7 q.choice_set.create(choice_text='The Clouds', votes=0)

    # 7 Display choices
    # 7 q.choice_set.all()

    # 7 Display number of choices
    # 7 q.choice_set.count()

    # 7 Show all choices for questions published this year
    # 7 Use __ to separate relationships
    # 7 Choice.objects.filter(question__pub_date__year=current_year)

    # 7 Delete a choice
    # 7 c = q.choice_set.filter(choice_text__startswith='The Clouds')

# 5 After defining the model we include the app in our project
# 5 under INSTALLED_APPS in settings.py
