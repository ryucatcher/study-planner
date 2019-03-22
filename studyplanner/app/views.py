from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

# Create your views here.
from .models import User

def index(request):
    user_list = User.objects.all()
    context = {
        'user_list': user_list
    }
    return render(request, 'index.html', context)

def createTask(request):
    return render(request, 'createTask.html')