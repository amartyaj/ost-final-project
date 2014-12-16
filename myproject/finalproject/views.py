# Create your views here.
#from django import http
from django import template
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.shortcuts import render_to_response
from google.appengine.ext import db
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from myproject.finalproject import djangoforms
from myproject.finalproject import models

import datetime
import time
#import urllib
import re
#import string
#import html
#import cgi
#import httplib
from google.appengine.api import users

def home(request):
    q = models.Question.all().order('-date_modified')
    #q_gql = models.Question.gql("WHERE question_tags = 'First'")

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

    time.sleep(0.1)
    q = models.Question.all().order('-date_modified')
    count = q.count()
    q_tags = []
    for i in models.Question.all():
        for j in i.question_tags:
            q_tags.append(j)
        #q_tags = set(q_tags)
        #q_tags = list(q_tags)
    #for i in q_gql:
        #for j in i.question_tags:
            #j.decode('utf8')
            #q_tags.append(j)
    q_tags = set(q_tags)
    q_tags = list(q_tags)

    images = models.Images.all().order('-date_uploaded')
    image_count = images.count()

    paginator = Paginator(q, 10)
    page = request.GET.get('page')
    try:
        question_pages = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        question_pages = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        question_pages = paginator.page(paginator.num_pages)

    return render_to_response('finalproject/index.html', {
        'questions': q,
        'question_pages': question_pages,
        'count': count,
        'context': context,
        'tags': q_tags,
        'images': images,
        'image_count': image_count,
    }, template.RequestContext(request))

def tag_questions(request, tag=None):
    #q = models.Question.all().order('-date_modified')
    q = models.Question.gql("WHERE question_tags = :param ORDER BY date_modified DESC", param=tag)
    #q = q.order('-date_modified')

    paginator = Paginator(q, 10)
    page = request.GET.get('page')
    try:
        question_pages = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        question_pages = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        question_pages = paginator.page(paginator.num_pages)

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

    return render_to_response('finalproject/tag_questions.html', {
        'questions': q,
        'question_pages': question_pages,
        'count': count,
        'context': context,
        'tag': tag,
    }, template.RequestContext(request))

def rss_feed(request, question_id=None):
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

    time.sleep(0.1)
    q = models.Question
    q = q.get_by_id(int(question_id))
    a = db.Query(models.Answers)
    a.filter('question', q)
    a.order('-total_votes')
    count = a.count()
    r1 = re.compile(r"(https?://[^\s]+(\.png|\.jpg|\.gif))")
    q.question_text = r1.sub(r'<img src="\1" >', q.question_text)
    #r2 = re.compile(r"(^https?://[^ ]+(\.png|\.jpg|\.gif))")
    #q.question_text = r2.sub(r'<img src="\1">', q.question_text)
    #r3 = re.compile(r" (https?://[^ ]+)")
    #q.question_text = r3.sub(r' <a href=" \1">\1</a>', q.question_text)
    #r4 = re.compile(r"(^https?://[^ ]+)")
    #q.question_text = r4.sub(r'<a href="\1">\1</a>', q.question_text)
    r2 = re.compile(r"(?<!\")(https?://[^\s]+)")
    q.question_text = r2.sub(r'<a href="\1">\1</a>', q.question_text)
    return render_to_response('finalproject/rss_feed.rss', {
        'question': q,
        'answers': a,
        'count': count,
        'context': context,
    }, template.RequestContext(request))

class QuestionForm(djangoforms.ModelForm):
    class Meta:
        model = models.Question
        exclude = ["short_question", "date_modified", "total_votes", "question_tags"]

def add_question_login_form(request):
    q = models.Question.all().order('-date_modified')
    count = q.count()

    paginator = Paginator(q, 10)
    page = request.GET.get('page')
    try:
        question_pages = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        question_pages = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        question_pages = paginator.page(paginator.num_pages)

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
                question_tmp = form.save(commit=False)
                question.short_question = question.question_text[:500]
                question.date_created = question.date_created + datetime.timedelta(hours=-5)
                question.date_modified = current_time
                if question_tmp.question_tag:
                    tags_list = question_tmp.question_tag.rstrip().split("\r\n")
                    #for tag in tags_list:
                        #tag = urllib.quote_plus(tag)
                        #tag = tag.strip()
                        #tag = tag.replace(" ", "")
                        #tag = tag.replace("\t", "")
                        #"".join(tag.split(string.whitespace))
                        #tag.strip(string.whitespace)
                    #tags_list = urllib.quote_plus(tags_list)
                    question.question_tag = question_tmp.question_tag
                    tags_list = set(tags_list)
                    tags_list = list(tags_list)
                    #question.question_tags = question.question_tags.append(str(question_tmp.question_tag))
                    #question.question_tags = [str(question_tmp.question_tag)]
                    question.question_tags = tags_list
                question.put()
                return HttpResponseRedirect('/questions')

        else:
            form = QuestionForm()

        time.sleep(0.1)
        q = models.Question.all().order('-date_modified')
        count = q.count()
        return render_to_response('finalproject/question_form.html', {
            'questions': q,
            'count': count,
            'form': form,
            'context': context,
        }, template.RequestContext(request))

    else:
        q_tags = []
        for i in models.Question.all():
            for j in i.question_tags:
                q_tags.append(j)
            #q_tags = set(q_tags)
            #q_tags = list(q_tags)
        #for i in q_gql:
            #for j in i.question_tags:
                #j.decode('utf8')
                #q_tags.append(j)
        q_tags = set(q_tags)
        q_tags = list(q_tags)

        images = models.Images.all().order('-date_uploaded')
        image_count = images.count()

        return render_to_response('finalproject/question_login_form.html', {
            'context': context,
            'question_pages': question_pages,
            'questions': q,
            'count': count,
            'tags': q_tags,
            'images': images,
            'image_count': image_count,
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

    if (user == models.Question.get_by_id(int(question_id)).created_by):
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
                question_tmp = form.save(commit=False)
                question.short_question = question.question_text[:500]
                #question.date_modified = question.date_modified + datetime.timedelta(hours=-5)
                question.date_modified = current_time

                if question_tmp.question_tag:
                    tags_list = question_tmp.question_tag.rstrip().split("\r\n")
                    question.question_tag = question_tmp.question_tag
                    tags_list = set(tags_list)
                    tags_list = list(tags_list)
                    question.question_tags = tags_list
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

        time.sleep(0.1)
        q = models.Question.all().order('-date_modified')
        count = q.count()
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

    time.sleep(0.1)
    q = models.Question
    q = q.get_by_id(int(question_id))
    a = db.Query(models.Answers)
    a.filter('question', q)
    a.order('-total_votes')
    count = a.count()
    r1 = re.compile(r"(https?://[^\s]+(\.png|\.jpg|\.gif))")
    q.question_text = r1.sub(r'<img src="\1" >', q.question_text)
    #r2 = re.compile(r"(^https?://[^ ]+(\.png|\.jpg|\.gif))")
    #q.question_text = r2.sub(r'<img src="\1">', q.question_text)
    #r3 = re.compile(r" (https?://[^ ]+)")
    #q.question_text = r3.sub(r' <a href=" \1">\1</a>', q.question_text)
    #r4 = re.compile(r"(^https?://[^ ]+)")
    #q.question_text = r4.sub(r'<a href="\1">\1</a>', q.question_text)
    r2 = re.compile(r"(?<!\")(https?://[^\s]+)")
    q.question_text = r2.sub(r'<a href="\1">\1</a>', q.question_text)
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
    a.order('-total_votes')
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
    r1 = re.compile(r"(?<!\")(https?://[^\s]+(\.png|\.jpg|\.gif))")
    q.question_text = r1.sub(r'<img src="\1" >', q.question_text)
    r2 = re.compile(r"(?<!\")(https?://[^\s]+)")
    q.question_text = r2.sub(r'<a href="\1">\1</a>', q.question_text)

    if user:
        if request.method == 'POST':
            form = AnswerForm(request.POST)

            if form.is_valid():
                answer = form.save(commit=False)
                answer.date_created = answer.date_created + datetime.timedelta(hours=-5)
                answer.date_modified = current_time
                answer.question = q
                r1 = re.compile(r"(?<!\")(https?://[^\s]+(\.png|\.jpg|\.gif))")
                answer.answer_text = r1.sub(r'<img src="\1" >', answer.answer_text)
                r2 = re.compile(r"(?<!\")(https?://[^\s]+)")
                answer.answer_text = r2.sub(r'<a href="\1">\1</a>', answer.answer_text)
                answer.put()
                return HttpResponseRedirect('/questions/%d' % int(question_id))

        else:
            form = AnswerForm()

        time.sleep(0.1)
        q = models.Question
        q = q.get_by_id(int(question_id))
        a = db.Query(models.Answers)
        a.filter('question', q)
        count = a.count()
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
            'answers': a,
            'count': count,
        }, template.RequestContext(request))

def edit_answer_login_form(request, answer_id=None):
    a = models.Answers
    a = a.get_by_id(int(answer_id))
    q = models.Question
    q = q.get_by_id(int(a.question.key().id()))
    all_a = db.Query(models.Answers)
    all_a.filter('question', q)
    all_a.order('-total_votes')
    #count = q.count()
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

    if (user == models.Answers.get_by_id(int(answer_id)).created_by):
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
                r1 = re.compile(r"(?<!\")(https?://[^\s]+(\.png|\.jpg|\.gif))")
                answer.answer_text = r1.sub(r'<img src="\1" >', answer.answer_text)
                r2 = re.compile(r"(?<!\")(https?://[^\s]+)")
                answer.answer_text = r2.sub(r'<a href="\1">\1</a>', answer.answer_text)
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

        time.sleep(0.1)
        a = models.Answers
        a = a.get_by_id(int(answer_id))
        return render_to_response('finalproject/answer_form.html', {
            'answers': a,
            #'count': count,
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
    a.order('-total_votes')
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
    r1 = re.compile(r"(?<!\")(https?://[^\s]+(\.png|\.jpg|\.gif))")
    q.question_text = r1.sub(r'<img src="\1" >', q.question_text)
    r2 = re.compile(r"(?<!\")(https?://[^\s]+)")
    q.question_text = r2.sub(r'<a href="\1">\1</a>', q.question_text)

    if user:
        question_tmp = models.Question.get_by_id(int(question_id))
        v = db.Query(models.QuestionVotes)
        v.filter('question', q)
        v.filter('created_by', user)
        v.order('-date_modified')
        v_tmp = v.get()
        up_vote_count = 0
        if v_tmp:
            if (v_tmp.vote == "Up"):
                up_vote_count = 1
        v = db.Query(models.QuestionVotes)
        v.filter('question', q)
        v.filter('created_by', user)
        v.order('-date_modified')
        v_tmp = v.get()
        down_vote_count = 0
        if v_tmp:
            if (v_tmp.vote == "Down"):
                down_vote_count = 1

        if (up_vote_count > 0):
            v1 = models.QuestionVotes(question=q, vote="Up", date_modified=current_time)
            v1.put()
        else:
            v1 = models.QuestionVotes(question=q, vote="Up", date_created=current_time, date_modified=current_time)
            v1.put()
            votes = q.total_votes
            if (down_vote_count > 0):
                votes = votes+2
            else:
                votes = votes+1
            if question_tmp.question_tag:
                tags_list = question_tmp.question_tag.rstrip().split("\r\n")
                q.question_tag = question_tmp.question_tag
                tags_list = set(tags_list)
                tags_list = list(tags_list)
                q.question_tags = tags_list
                q1 = models.Question(key=q.key(), created_by=q.created_by, date_created=q.date_created, modified_by=q.modified_by, date_modified=q.date_modified, short_question=q.short_question, question_text=q.question_text, question_tag=q.question_tag, question_tags=q.question_tags, total_votes=votes)
            else:
                q1 = models.Question(key=q.key(), created_by=q.created_by, date_created=q.date_created, modified_by=q.modified_by, date_modified=q.date_modified, short_question=q.short_question, question_text=q.question_text, total_votes=votes)
            q1.put()

        time.sleep(0.1)
        q = models.Question
        q = q.get_by_id(int(question_id))
        a = db.Query(models.Answers)
        a.filter('question', q)
        a.order('-total_votes')
        count = a.count()
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

def question_vote_down_login_form(request, question_id=None):
    q = models.Question
    q = q.get_by_id(int(question_id))
    a = db.Query(models.Answers)
    a.filter('question', q)
    a.order('-total_votes')
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
    r1 = re.compile(r"(?<!\")(https?://[^\s]+(\.png|\.jpg|\.gif))")
    q.question_text = r1.sub(r'<img src="\1" >', q.question_text)
    r2 = re.compile(r"(?<!\")(https?://[^\s]+)")
    q.question_text = r2.sub(r'<a href="\1">\1</a>', q.question_text)

    if user:
        question_tmp = models.Question.get_by_id(int(question_id))
        v = db.Query(models.QuestionVotes)
        v.filter('question', q)
        v.filter('created_by', user)
        v.order('-date_modified')
        v_tmp = v.get()
        up_vote_count = 0
        if v_tmp:
            if (v_tmp.vote == "Up"):
                up_vote_count = 1
        v = db.Query(models.QuestionVotes)
        v.filter('question', q)
        v.filter('created_by', user)
        v.order('-date_modified')
        v_tmp = v.get()
        down_vote_count = 0
        if v_tmp:
            if (v_tmp.vote == "Down"):
                down_vote_count = 1
        if (down_vote_count > 0):
            v1 = models.QuestionVotes(question=q, vote="Down", date_modified=current_time)
            v1.put()
        else:
            v1 = models.QuestionVotes(question=q, vote="Down", date_created=current_time, date_modified=current_time)
            v1.put()
            votes = q.total_votes
            if (up_vote_count > 0):
                votes = votes-2
            else:
                votes = votes-1
            if question_tmp.question_tag:
                tags_list = question_tmp.question_tag.rstrip().split("\r\n")
                q.question_tag = question_tmp.question_tag
                tags_list = set(tags_list)
                tags_list = list(tags_list)
                q.question_tags = tags_list
                q1 = models.Question(key=q.key(), created_by=q.created_by, date_created=q.date_created, modified_by=q.modified_by, date_modified=q.date_modified, short_question=q.short_question, question_text=q.question_text, question_tag=q.question_tag, question_tags=q.question_tags, total_votes=votes)
            else:
                q1 = models.Question(key=q.key(), created_by=q.created_by, date_created=q.date_created, modified_by=q.modified_by, date_modified=q.date_modified, short_question=q.short_question, question_text=q.question_text, total_votes=votes)
            q1.put()

        time.sleep(0.1)
        q = models.Question
        q = q.get_by_id(int(question_id))
        a = db.Query(models.Answers)
        a.filter('question', q)
        a.order('-total_votes')
        count = a.count()
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

class AnswerVotesForm(djangoforms.ModelForm):
    class Meta:
        model = models.AnswerVotes

def answer_vote_up_login_form(request, answer_id=None):
    ans = models.Answers
    ans = ans.get_by_id(int(answer_id))
    q = models.Question
    q = q.get_by_id(int(ans.question.key().id()))
    a = db.Query(models.Answers)
    a.filter('question', q)
    a.order('-total_votes')
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
    r1 = re.compile(r"(?<!\")(https?://[^\s]+(\.png|\.jpg|\.gif))")
    q.question_text = r1.sub(r'<img src="\1" >', q.question_text)
    r2 = re.compile(r"(?<!\")(https?://[^\s]+)")
    q.question_text = r2.sub(r'<a href="\1">\1</a>', q.question_text)

    if user:
        v = db.Query(models.AnswerVotes)
        v.filter('answer', ans)
        v.filter('created_by', user)
        v.order('-date_modified')
        v_tmp = v.get()
        up_vote_count = 0
        if v_tmp:
            if (v_tmp.vote == "Up"):
                up_vote_count = 1
        v = db.Query(models.AnswerVotes)
        v.filter('answer', ans)
        v.filter('created_by', user)
        v.order('-date_modified')
        v_tmp = v.get()
        down_vote_count = 0
        if v_tmp:
            if (v_tmp.vote == "Down"):
                down_vote_count = 1

        if (up_vote_count > 0):
            v1 = models.AnswerVotes(answer=ans, vote="Up", date_modified=current_time)
            v1.put()
        else:
            v1 = models.AnswerVotes(answer=ans, vote="Up", date_created=current_time, date_modified=current_time)
            v1.put()
            votes = ans.total_votes
            if (down_vote_count > 0):
                votes = votes+2
            else:
                votes = votes+1
            a1 = models.Answers(key=ans.key(), question=ans.question, created_by=ans.created_by, date_created=ans.date_created, modified_by=ans.modified_by, date_modified=ans.date_modified, answer_text=ans.answer_text, total_votes=votes)
            a1.put()

        time.sleep(0.1)
        ans = models.Answers
        ans = ans.get_by_id(int(answer_id))
        q = models.Question
        q = q.get_by_id(int(ans.question.key().id()))
        a = db.Query(models.Answers)
        a.filter('question', q)
        a.order('-total_votes')
        count = a.count()
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

def answer_vote_down_login_form(request, answer_id=None):
    ans = models.Answers
    ans = ans.get_by_id(int(answer_id))
    q = models.Question
    q = q.get_by_id(int(ans.question.key().id()))
    a = db.Query(models.Answers)
    a.filter('question', q)
    a.order('-total_votes')
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
    r1 = re.compile(r"(?<!\")(https?://[^\s]+(\.png|\.jpg|\.gif))")
    q.question_text = r1.sub(r'<img src="\1" >', q.question_text)
    r2 = re.compile(r"(?<!\")(https?://[^\s]+)")
    q.question_text = r2.sub(r'<a href="\1">\1</a>', q.question_text)

    if user:
        v = db.Query(models.AnswerVotes)
        v.filter('answer', ans)
        v.filter('created_by', user)
        v.order('-date_modified')
        v_tmp = v.get()
        up_vote_count = 0
        if v_tmp:
            if (v_tmp.vote == "Up"):
                up_vote_count = 1
        v = db.Query(models.AnswerVotes)
        v.filter('answer', ans)
        v.filter('created_by', user)
        v.order('-date_modified')
        v_tmp = v.get()
        down_vote_count = 0
        if v_tmp:
            if (v_tmp.vote == "Down"):
                down_vote_count = 1

        if (down_vote_count > 0):
            v1 = models.AnswerVotes(answer=ans, vote="Down", date_modified=current_time)
            v1.put()
        else:
            v1 = models.AnswerVotes(answer=ans, vote="Down", date_created=current_time, date_modified=current_time)
            v1.put()
            votes = ans.total_votes
            if (up_vote_count > 0):
                votes = votes-2
            else:
                votes = votes-1
            a1 = models.Answers(key=ans.key(), question=ans.question, created_by=ans.created_by, date_created=ans.date_created, modified_by=ans.modified_by, date_modified=ans.date_modified, answer_text=ans.answer_text, total_votes=votes)
            a1.put()

        time.sleep(0.1)
        ans = models.Answers
        ans = ans.get_by_id(int(answer_id))
        q = models.Question
        q = q.get_by_id(int(ans.question.key().id()))
        a = db.Query(models.Answers)
        a.filter('question', q)
        a.order('-total_votes')
        count = a.count()
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

class ImageForm(djangoforms.ModelForm):
    class Meta:
        model = models.Images

def upload_image(request):
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

    form = ImageForm(request.POST, request.FILES)
    q = models.Question.all().order('-date_modified')
    count = q.count()

    paginator = Paginator(q, 10)
    page = request.GET.get('page')
    try:
        question_pages = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        question_pages = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        question_pages = paginator.page(paginator.num_pages)

    q_tags = []
    for i in models.Question.all():
        for j in i.question_tags:
            q_tags.append(j)
        #q_tags = set(q_tags)
        #q_tags = list(q_tags)
    #for i in q_gql:
        #for j in i.question_tags:
            #j.decode('utf8')
            #q_tags.append(j)
    q_tags = set(q_tags)
    q_tags = list(q_tags)
    images = models.Images.all().order('-date_uploaded')
    image_count = images.count()

    if user:
        images = form.save(commit=False)
        img_name = request.FILES['image'].name
        img = request.FILES['image'].read()
        images.image = db.Blob(img)
        images.date_uploaded = current_time
        images.name = img_name
        images.put()
        return HttpResponseRedirect('/questions')
            # else fall through to redisplay the form with error messages

        time.sleep(0.1)
        q = models.Question.all().order('-date_modified')
        count = q.count()
        return render_to_response('finalproject/index.html', {
            'context': context,
            'question_pages': question_pages,
            'questions': q,
            'count': count,
            'tags': q_tags,
            'images': images,
            'image_count': image_count,
        }, template.RequestContext(request))

    else:
        return render_to_response('finalproject/image_login_form.html', {
            'context': context,
            'question_pages': question_pages,
            'questions': q,
            'count': count,
            'tags': q_tags,
            'images': images,
            'image_count': image_count,
        }, template.RequestContext(request))

def retrieve_image(request, image_id=None):
    images = models.Images
    image_instance = images.get_by_id(int(image_id))
    image = image_instance.image
    image_name = image_instance.name
    if (re.findall("\.png$", image_name)):
        return HttpResponse(image, mimetype="image/png")
    if (re.findall("\.gif$", image_name)):
        return HttpResponse(image, mimetype="image/gif")
    if (re.findall("\.jpg$", image_name)):
        return HttpResponse(image, mimetype="image/jpg")
    if (re.findall("\.jpeg$", image_name)):
        return HttpResponse(image, mimetype="image/jpeg")

    #return render_to_response('finalproject/retrieve_image.html', {
        #'context': context,
        #'image_instance': image_instance,
        #'image': image,
        #}, template.RequestContext(request))

