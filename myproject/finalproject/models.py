#from django.db import models
# Create your models here.
from google.appengine.ext import db

class Question(db.Model):
    title = db.StringProperty(verbose_name="Question title")
    author = db.StringProperty()
    copyright_year = db.IntegerProperty()
    author_birthdate = db.DateProperty()

class QuestionReview(db.Model):
    question = db.ReferenceProperty(Question, collection_name='reviews')
    review_author = db.UserProperty()
    review_text = db.TextProperty()
    rating = db.StringProperty(choices=['Poor', 'OK', 'Good', 'Very Good', 'Great'],
                               default='Great')
    create_date = db.DateTimeProperty(auto_now_add=True)
