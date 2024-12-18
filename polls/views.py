from django.shortcuts import render
from django.http import HttpResponse  # HttpResponse import 추가

# Create your views here.

def index(request):
    return HttpResponse("Hello, world.")

