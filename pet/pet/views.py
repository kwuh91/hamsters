from django.shortcuts import render
from django.http import HttpResponseNotFound

# Create your views here.

def pageNotFound(request, exception):
    return HttpResponseNotFound("<h1>Page not found</h1>")
