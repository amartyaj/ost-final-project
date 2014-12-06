# Create your views here.
from django import http

def home(request):
    return http.HttpResponse('Welcome to the question answer forum!')
