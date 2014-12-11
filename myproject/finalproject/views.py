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
    q = models.Question.all().order('-date_modified')
    count = q.count()
    current_time = datetime.datetime.now() + datetime.timedelta(hours=-5)
    user = users.get_current_user()
    login_url = users.create_login_url(request.path)
    logout_url = users.create_logout_url(request.path)
    context = {
        'current_time': current_time,
        'user': user,
        'login_url': login_url,
        'logout_url': logout_url,
    }

    return render_to_response('finalproject/index.html', {
        'questions': q,
        'count': count,
        'context': context,
    }, template.RequestContext(request))

class QuestionForm(djangoforms.ModelForm):
    class Meta:
        model = models.Question
        exclude = ["short_question", "date_modified", "total_votes"]

def add_question_login_form(request):
    q = models.Question.all().order('-date_modified')
    count = q.count()
    current_time = datetime.datetime.now() + datetime.timedelta(hours=-5)
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
            form = QuestionForm(request.POST)

            if form.is_valid():
                question = form.save(commit=False)
                question.short_question = question.question_text[:500]
                question.date_created = question.date_created + datetime.timedelta(hours=-5)
                question.date_modified = current_time
                question.put()
                return HttpResponseRedirect('/questions')

        else:
            form = QuestionForm()

        return render_to_response('finalproject/question_form.html', {
            'questions': q,
            'count': count,
            'form': form,
            'context': context,
        }, template.RequestContext(request))

    else:
        return render_to_response('finalproject/question_login_form.html', {
            'context': context,
            'questions': q,
            'count': count,
        }, template.RequestContext(request))

def edit_question_login_form(request, question_id=None):
    q = models.Question.all().order('-date_modified')
    count = q.count()
    current_time = datetime.datetime.now() + datetime.timedelta(hours=-5)
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
            if question_id:
                # Fetch the existing Question and update it from the form.
                question = models.Question.get_by_id(int(question_id))
                question.short_question = question.question_text[:500]
                form = QuestionForm(request.POST, instance=question)
            else:
                # Create a new Question based on the form.
                form = QuestionForm(request.POST)

            if form.is_valid():
                question = form.save(commit=False)
                question.short_question = question.question_text[:500]
                #question.date_modified = question.date_modified + datetime.timedelta(hours=-5)
                question.date_modified = current_time
                question.put()
                return HttpResponseRedirect('/questions')
            # else fall through to redisplay the form with error messages

        else:
            # The user wants to see the form.
            if question_id:
                # Show the form to edit an existing Question.
                question = models.Question.get_by_id(int(question_id))
                question.short_question = question.question_text[:500]
                form = QuestionForm(instance=question)
            else:
                # Show the form to create a new Question.
                form = QuestionForm()

        return render_to_response('finalproject/question_form.html', {
            'questions': q,
            'count': count,
            'question_id': question_id,
            'form': form,
            'context': context,
        }, template.RequestContext(request))

    else:
        return render_to_response('finalproject/question_login_form.html', {
            'context': context,
            'questions': q,
            'count': count,
        }, template.RequestContext(request))

def view_question(request, question_id=None):
    q = models.Question
    q = q.get_by_id(int(question_id))
    a = db.Query(models.Answers)
    a.filter('question', q)
    count = a.count()
    current_time = datetime.datetime.now() + datetime.timedelta(hours=-5)
    user = users.get_current_user()
    login_url = users.create_login_url(request.path)
    logout_url = users.create_logout_url(request.path)
    context = {
        'current_time': current_time,
        'user': user,
        'login_url': login_url,
        'logout_url': logout_url,
    }

    return render_to_response('finalproject/view_question.html', {
        'question': q,
        'answers': a,
        'count': count,
        'context': context,
    }, template.RequestContext(request))

class AnswerForm(djangoforms.ModelForm):
    class Meta:
        model = models.Answers
        exclude = ["question", "date_modified", "total_votes"]

def add_answer_login_form(request, question_id=None):
    q = models.Question
    q = q.get_by_id(int(question_id))
    a = db.Query(models.Answers)
    a.filter('question', q)
    count = a.count()
    current_time = datetime.datetime.now() + datetime.timedelta(hours=-5)
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
            form = AnswerForm(request.POST)

            if form.is_valid():
                answer = form.save(commit=False)
                answer.date_created = answer.date_created + datetime.timedelta(hours=-5)
                answer.date_modified = current_time
                answer.question = q
                answer.put()
                return HttpResponseRedirect('/questions/%d' % int(question_id))

        else:
            form = AnswerForm()

        return render_to_response('finalproject/answer_form.html', {
            'question': q,
            'answers': a,
            'count': count,
            'form': form,
            'context': context,
        }, template.RequestContext(request))

    else:
        return render_to_response('finalproject/answer_login_form.html', {
            'context': context,
            'question': q,
            'all_answers': a,
            'count': count,
        }, template.RequestContext(request))

def edit_answer_login_form(request, answer_id=None):
    a = models.Answers
    a = a.get_by_id(int(answer_id))
    q = models.Question
    q = q.get_by_id(int(a.question.key().id()))
    all_a = db.Query(models.Answers)
    all_a.filter('question', q)
#    count = q.count()
    current_time = datetime.datetime.now() + datetime.timedelta(hours=-5)
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
            if answer_id:
                # Fetch the existing Question and update it from the form.
                answer = models.Answers.get_by_id(int(answer_id))
                form = AnswerForm(request.POST, instance=answer)
            else:
                # Create a new Question based on the form.
                form = AnswerForm(request.POST)

            if form.is_valid():
                answer = form.save(commit=False)
                #question.short_question = question.question_text[:500]
                answer.date_created = answer.date_created + datetime.timedelta(hours=-5)
                answer.date_modified = current_time
                answer.put()
                return HttpResponseRedirect('/questions/%d' % answer.question.key().id())
            # else fall through to redisplay the form with error messages

        else:
            # The user wants to see the form.
            if answer_id:
                # Show the form to edit an existing Question.
                answer = models.Answers.get_by_id(int(answer_id))
                form = AnswerForm(instance=answer)
            else:
                # Show the form to create a new Question.
                form = AnswerForm()

        return render_to_response('finalproject/answer_form.html', {
            'answers': a,
#            'count': count,
            'answer_id': answer_id,
            'form': form,
            'context': context,
        }, template.RequestContext(request))

    else:
        return render_to_response('finalproject/answer_login_form.html', {
            'context': context,
            'answers': a,
            'question': q,
            'all_answers': all_a,
            'answer_id': answer_id,
        }, template.RequestContext(request))

class QuestionVotesForm(djangoforms.ModelForm):
    class Meta:
        model = models.QuestionVotes

def question_vote_up_login_form(request, question_id=None):
    q = models.Question
    q = q.get_by_id(int(question_id))
    a = db.Query(models.Answers)
    a.filter('question', q)
    count = a.count()
    current_time = datetime.datetime.now() + datetime.timedelta(hours=-5)
    user = users.get_current_user()
    login_url = users.create_login_url(request.path)
    logout_url = users.create_logout_url(request.path)
    context = {
        'current_time': current_time,
        'user': user,
        'login_url': login_url,
        'logout_url': logout_url,
    }

    v = db.Query(models.QuestionVotes)
    v.filter('question', q)
    v.filter('created_by', user)
    vote_count = v.count()
#    question_votes = models.QuestionVotes.get_by_id(v.key().id())
#    v1 = models.QuestionVotes(instance=question_votes)
#    if (vote_count > 0):
#        question_votes = models.QuestionVotes.get_by_id(v.key().id())
#        form = QuestionVotesForm(instance=question_votes)
#    else:
#        question_votes = models.QuestionVotes
#        form = QuestionVotesForm(instance=question_votes)
#    question_votes = form.save(commit=False)
    if (vote_count > 0):
        v.vote = "Up"
#        v.date_created = question_votes.date_created + datetime.timedelta(hours=-5)
        v.date_modified = current_time
    else:
#        v1.question = q
#        v1.vote = "Up"
#        v1.date_created = current_time
#        v1.date_modified = current_time

        v1 = models.QuestionVotes(question=q, vote="Up", date_created=current_time, date_modified=current_time)
        v1.put()

    if user:
        #form = QuestionForm(instance=q)
        return render_to_response('finalproject/view_question.html', {
            'question': q,
            'answers': a,
            'count': count,
            'context': context,
        }, template.RequestContext(request))

    else:
        return render_to_response('finalproject/vote_login_form.html', {
            'question': q,
            'answers': a,
            'count': count,
            'context': context,
        }, template.RequestContext(request))

#def question_vote_down_login_form(request, question_id=None):
#def answer_vote_up_login_form(request, answer_id=None):
#def answer_vote_down_login_form(request, answer_id=None):
