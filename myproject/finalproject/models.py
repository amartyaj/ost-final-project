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

class Answers(db.Model):
    question = db.ReferenceProperty(Question, collection_name='answers')
    created_by = db.UserProperty(auto_current_user_add=True)
    date_created = db.DateTimeProperty(auto_now_add=True)
    modified_by = db.UserProperty(auto_current_user=True)
    #date_modified = db.DateTimeProperty(auto_now=True)
    date_modified = db.DateTimeProperty()
    answer_text = db.TextProperty(required=True)

#class Question_votes(db.Model):
#class Answer_votes(db.Model):
#class Question_tags(db.Model):
#class Question_followers(db.Model):

class QuestionReview(db.Model):
    question = db.ReferenceProperty(Question, collection_name='reviews')
    review_author = db.UserProperty()
    review_text = db.TextProperty()
    rating = db.StringProperty(choices=['Poor', 'OK', 'Good', 'Very Good', 'Great'],
                               default='Great')
    create_date = db.DateTimeProperty(auto_now_add=True)
