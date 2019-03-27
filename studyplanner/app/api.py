from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

# Create your views here.
from .models import User

def updateDeadlineName(request):
    return HttpResponse()