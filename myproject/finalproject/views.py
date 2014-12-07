# Create your views here.
#from django import http
from django import template
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from google.appengine.ext import db

from myproject.finalproject import djangoforms
from myproject.finalproject import models

import datetime
from google.appengine.api import users

def home(request):
    q = models.Question.all().order('title')
    return render_to_response('finalproject/index.html',
                              { 'questions': q })

class QuestionForm(djangoforms.ModelForm):
    class Meta:
        model = models.Question

def question_form(request, question_id=None):
    if request.method == 'POST':
        # The form was submitted.
        if question_id:
            # Fetch the existing Question and update it from the form.
            question = models.Question.get_by_id(int(question_id))
            form = QuestionForm(request.POST, instance=question)
        else:
            # Create a new Question based on the form.
            form = QuestionForm(request.POST)

        if form.is_valid():
            question = form.save(commit=False)
            question.put()
            return HttpResponseRedirect('/questions/')
        # else fall through to redisplay the form with error messages

    else:
        # The user wants to see the form.
        if question_id:
            # Show the form to edit an existing Question.
            question = models.Question.get_by_id(int(question_id))
            form = QuestionForm(instance=question)
        else:
            # Show the form to create a new Question.
            form = QuestionForm()

    return render_to_response('finalproject/question_form.html', {
        'question_id': question_id,
        'form': form,
    }, template.RequestContext(request))

def add_question_login_form(request, question_id=None):
    current_time = datetime.datetime.now()
    user = users.get_current_user()
    login_url = users.create_login_url(request.path)
    logout_url = users.create_logout_url(request.path)
    context = {
        'current_time': current_time,
        'user': user,
        'login_url': login_url,
        'logout_url': logout_url,
    }

    if user:
        if request.method == 'POST':
            # The form was submitted.
            if question_id:
                # Fetch the existing Question and update it from the form.
                question = models.Question.get_by_id(int(question_id))
                form = QuestionForm(request.POST, instance=question)
            else:
                # Create a new Question based on the form.
                form = QuestionForm(request.POST)

            if form.is_valid():
                question = form.save(commit=False)
                question.put()
                return HttpResponseRedirect('/questions/')
            # else fall through to redisplay the form with error messages

        else:
            # The user wants to see the form.
            if question_id:
                # Show the form to edit an existing Question.
                question = models.Question.get_by_id(int(question_id))
                form = QuestionForm(instance=question)
            else:
                # Show the form to create a new Question.
                form = QuestionForm()

        return render_to_response('finalproject/question_form.html', {
            'question_id': question_id,
            'form': form,
        }, template.RequestContext(request))

    else:
        return render_to_response('finalproject/login_form.html', context, template.RequestContext(request))
