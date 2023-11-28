from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return HttpResponse("Hello, this is your app's home!")
# Create your views here.
