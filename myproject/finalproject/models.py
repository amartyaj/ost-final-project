#from django.db import models
# Create your models here.
from google.appengine.ext import db

class Question(db.Model):
    created_by = db.UserProperty(auto_current_user_add=True)
    date_created = db.DateTimeProperty(auto_now_add=True)
    modified_by = db.UserProperty(auto_current_user=True)
    #date_modified = db.DateTimeProperty(auto_now=True)
    date_modified = db.DateTimeProperty()
    short_question = db.StringProperty(multiline=True)
    question_text = db.TextProperty(required=True)
    total_votes = db.IntegerProperty(default=0)
    question_tags = db.StringListProperty()

class Answers(db.Model):
    question = db.ReferenceProperty(Question, collection_name='answers')
    created_by = db.UserProperty(auto_current_user_add=True)
    date_created = db.DateTimeProperty(auto_now_add=True)
    modified_by = db.UserProperty(auto_current_user=True)
    #date_modified = db.DateTimeProperty(auto_now=True)
    date_modified = db.DateTimeProperty()
    answer_text = db.TextProperty(required=True)
    total_votes = db.IntegerProperty(default=0)

class QuestionVotes(db.Model):
    question = db.ReferenceProperty(Question, collection_name='question_votes')
    created_by = db.UserProperty(auto_current_user_add=True)
    date_created = db.DateTimeProperty(auto_now_add=True)
    modified_by = db.UserProperty(auto_current_user=True)
    #date_modified = db.DateTimeProperty(auto_now=True)
    date_modified = db.DateTimeProperty()
    vote = db.StringProperty(choices=['Up', 'Down'])

class AnswerVotes(db.Model):
    answer = db.ReferenceProperty(Answers, collection_name='answer_votes')
    created_by = db.UserProperty(auto_current_user_add=True)
    date_created = db.DateTimeProperty(auto_now_add=True)
    modified_by = db.UserProperty(auto_current_user=True)
    #date_modified = db.DateTimeProperty(auto_now=True)
    date_modified = db.DateTimeProperty()
    vote = db.StringProperty(choices=['Up', 'Down'])

#class Question_tags(db.Model):
#class Question_followers(db.Model):
