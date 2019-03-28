from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.middleware import csrf
from django.shortcuts import redirect

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
        'csrf': csrf.get_token(request)
    }
    return render(request, 'dashboardtest.html', context)

def uploadHubFile(request):

    return redirect('/dashboard')
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

def task(request):
    activities = [
        {'name' : 'activity 1', 'progress' : 100, 'type' : 'Programming'},
        {'name' : 'activity 2', 'progress' : 50, 'type' : 'Studying' },
        {'name' : 'activity 3', 'progress' : 15, 'type' : 'Writing' }
    ]
    numActivs = len(activities)
    progress = 0
    for a in activities:
        progress += a["progress"]/numActivs
    progress = int(progress)
    notes = [
        {'note' : 'note 1', 'date' : '13/03/2019' },
        {'note' : '2 note 2 furious', 'date' : '14/03/2019' },
        {'note' : 'A longer note, with a lot of text, so much text, a lot of things', 'date' : '16/03/2019' },
        {'note' : 'note 4', 'date' : '17/03/2019' }
    ]
    requiredTasks = [
        {'name' : 'Another task 1'}, {'name' : 'Another task 2'},
    ]
    task = {
        'name' : 'Some task name',
        'assessment' : 'Software Engineering 1 Coursework',
        'duration' : '5 days',
        'description' : '',
        'progress' : progress,
        'activities' : activities,
        'notes' : notes,
        'tasks' : requiredTasks,
    }
    context = {
        'navigation': navigation_list,
        'active': 'Deadlines',
        'task' : task
    }
    return render(request, 'task.html', context)

def activity(request):
    notes = [
        {'note' : 'note 1', 'date' : '13/03/2019' },
        {'note' : '2 note 2 furious', 'date' : '14/03/2019' },
        {'note' : 'A longer note, with a lot of text, so much text, a lot of things', 'date' : '16/03/2019' },
        {'note' : 'note 4', 'date' : '17/03/2019' }
    ]
    tasks = [
        {'name' : 'Another task 1'}, {'name' : 'Another task 2'},
    ]
    activity = {
        'name' : 'Some activity name',
        'assessment' : 'Software Engineering 1 Coursework',
        'type' : 'Programming',
        'progress' : 80,
        'completed' : 8,
        'target' : 10,
        'units' : 'requirements',
        'notes' : notes,
        'tasks' : tasks,
    }
    context = {
        'navigation': navigation_list,
        'active': 'Deadlines',
        'activity' : activity
    }
    return render(request, 'activity.html', context)
