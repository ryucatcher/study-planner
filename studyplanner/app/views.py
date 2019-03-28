from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

# Create your views here.
from .models import User

navigation_list = [
    {'icon': 'img/icon_deadlines.png', 'title': 'Deadlines', 'url': '/deadlines'},
    {'icon': 'img/icon_modules.png', 'title': 'Modules', 'url': '/modules'},
    {'icon': 'img/icon_gantt.png', 'title': 'Gantt Chart', 'url': '/ganttchart'},
    {'icon': 'img/icon_add.png', 'title': 'Add Task', 'url': '/addtask'},
    {'icon': 'img/icon_logout.png', 'title': 'Logout', 'url': '/logout'}
]


def index(request):
    user_list = User.objects.all()
    context = {
        'user_list': user_list
    }
    return render(request, 'index.html', context)


def dashboard(request):
    context = {
        'navigation': navigation_list,
        'active': 'Deadlines',
    }
    return render(request, 'dashboardtest.html', context)

def deadlines(request):
    upcoming = [
        {'name':'Software Engineering coursework 2', 'date':'15/04/2019','progress':30},
        {'name':'Graphics Coursework', 'date':'26/04/2019','progress':0},
        {'name':'Programming coursework 2', 'date':'01/05/2019','progress':90}
    ]
    inprogress = [
        {'name':'Software Engineering coursework 2', 'date':'15/04/2019','progress':30},
        {'name':'Programming coursework 2', 'date':'01/05/2019','progress':90}
    ]
    missed = [
        {'name':'Database Structures and Algorithms coursework', 'date':'20/03/2019','progress':80}
    ]
    completed = [
        {'name':'Software Engineering coursework 1', 'date':'15/03/2019','progress':100},
        {'name':'Programming coursework 1', 'date':'26/02/2019','progress':100},
        {'name':'Programming coursework 1', 'date':'26/02/2019','progress':100},
        {'name':'Programming coursework 1', 'date':'26/02/2019','progress':100},
        {'name':'Programming coursework 1', 'date':'26/02/2019','progress':100}
    ]
    context = {
        'navigation': navigation_list,
        'active': 'Deadlines',
        'upcoming' : upcoming,
        'inprogress' : inprogress,
        'missed' : missed,
        'completed' : completed
    }
    return render(request, 'deadlines.html', context)

def assessment(request):
    tasks = [
        {'name' : 'task 1', 'progress' : 80 },
        {'name' : 'task 2', 'progress' : 60 },
        {'name' : 'task 3', 'progress' : 30 }
    ]
    numTasks = len(tasks)
    progress = 0
    for t in tasks:
        progress += t["progress"]/numTasks
    progress = int(progress)
    assessment = {
        'name' : 'Software Engineering 1 Coursework',
        'type' : 'Coursework',
        'module' : 'Software Engineering',
        'startdate' : '15/01/2019',
        'deadline' : '13/03/2019',
        'weight' : 40,
        'description' : 'Assessment description',
        'progress' : progress,
        'tasks' : tasks
    }
    context = {
        'navigation': navigation_list,
        'active': 'Deadlines',
        'assessment' : assessment
    }
    return render(request, 'assessment.html', context)
