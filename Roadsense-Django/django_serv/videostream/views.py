from django.shortcuts import render
from django.http import HttpResponse

from django.http import StreamingHttpResponse
import cv2
import threading
import time
import requests

def home(request):
    return HttpResponse("Hello, this is your app's home!")

