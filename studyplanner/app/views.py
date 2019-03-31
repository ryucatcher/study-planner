from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.middleware import csrf
from django.shortcuts import redirect

import json
from datetime import datetime

# Create your views here.
from .models import *

navigation_list = [
    {'icon': 'img/icon_deadlines.png', 'title': 'Deadlines', 'url': '/deadlines'},
    {'icon': 'img/icon_modules.png', 'title': 'Modules', 'url': '/modules'},
    {'icon': 'img/icon_gantt.png', 'title': 'Gantt Chart', 'url': '/ganttchart'},
    {'icon': 'img/icon_add.png', 'title': 'Add Task', 'url': '/addtask'},
    {'icon': 'img/icon_logout.png', 'title': 'Logout', 'url': '/logout'}
]

def isLoggedIn(request):
    if 'userid' in request.COOKIES:
        return True
    return False

def isValidEmail(email):
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False

def isValidPassword(password):
    return len(password) > 7

def loginUser(response, userid):
    response.set_cookie('userid', userid)

def index(request):
    user_list = User.objects.all()
    context = {
        'user_list': user_list
    }
    return render(request, 'index.html', context)


def login(request):
    # If user already logged in
    if isLoggedIn(request):
        return redirect('/dashboard')
    
    # error context
    context = {}
    if 'error' in request.GET:
        context['error'] = request.GET['error']

    return render(request,'login.html', context)

def processLogin(request):
    email = request.POST['email']
    if not isValidEmail(email):
        print('Invalid email.')
        return redirect('/error=Invalid Email')
    
    user = User.objects.filter(email=email)

    if len(user) == 0:
        print('User does not exist.')
        return redirect('/?error=User does not exist.')

    user = user[0]

    password = request.POST['password']
    
    if user.password != password:
        print('Wrong password!')
        return redirect('/?error=Wrong password.')

    # User login should be verified now
    print('Login success!')

    # Set logged in cookie
    response = redirect('/')
    loginUser(response, user.userid)

    return response

def createAccount(request):
    if isLoggedIn(request):
        return redirect('/dashboard')
    context = {}
    if 'error' in request.GET:
        context['error'] = request.GET['error']
    return render(request, 'createaccount.html', context)

def processAccount(request):
    post = request.POST
    response = redirect('/')
    if post['action'] == 'createaccount':
        email = post['email']
        if not isValidEmail(email):
            return redirect('/createaccount?error=Invalid email')

        fname = post['fname']
        lname = post['lname']
        if len(fname) == 0 or len(lname) == 0:
            return redirect('/createaccount?error=Names must not be empty')

        password = post['password']
        if not isValidPassword(password):
            return redirect('/createaccount?error=Password must be at least 8 characters long')
        
        # User data is valid so create account
        user = User(email=email, firstname=fname, lastname=lname, password=password)
        response = redirect('/')
        try:
            user.save()
            loginUser(response, user.userid)
        except Exception as e:
            return redirect('/createaccount?error=' + e)

    return response

def logout(request):
    response = redirect('/')
    response.delete_cookie('userid')
    return response

def dashboard(request):
    context = {
        'navigation': navigation_list,
        'active': 'Deadlines',
        'csrf': csrf.get_token(request)
    }
    return render(request, 'dashboardtest.html', context)

def _createSemesterStudyProfile(request, content, userid):
    user = User.objects.get(userid=userid)

    # Delete existing profile with the same year
    SemesterStudyProfile.objects.filter(user=user, year=content['Year']).delete()
    
    profile = SemesterStudyProfile(year=content['Year'], semester=content['Semester'], user=user)
    profile.save()
    # Add modules to study profile
    for m in content['Modules']:
        module = Module(name=m['Name'], code=m['Code'], description=m['Description'], semester=profile)
        module.save()
        # Add assessments to modules
        DTFORMAT = '%d-%m-%Y'
        for a in m['Assessments']:
            assessmentType = AssessmentType.CW if a['Type'] == 'cw' else AssessmentType.EX
            if assessmentType == AssessmentType.CW:    
                startdate = datetime.strptime(a['startdate'], DTFORMAT).date()
                enddate = datetime.strptime(a['enddate'], DTFORMAT).date()
                assessment = Assessment(weight=a['weight'], startDate=startdate, deadline=enddate, assessmentType=assessmentType, module=module)
            else:
                date = datetime.strptime(a['date'], DTFORMAT).date()
                assessment = Assessment(weight=a['weight'], startDate=date, deadline=date, assessmentType=assessmentType, module=module)
            assessment.save()
            
def uploadHubFile(request):
    # If user is not logged in, redirect to login page
    if not isLoggedIn(request):
        return redirect('/')
    
    userid = request.COOKIES['userid']
    if request.method == 'POST':
        file = request.FILES['hubfile']
        contentString = file.read()
        contentJSON = json.loads(contentString)
        _createSemesterStudyProfile(request, contentJSON, userid)

    return redirect('/dashboard')


def deadlines(request):
    deadlines = Assessment.objects.all()
    upcoming = list()
    for dl in deadlines:
        p = int(dl.progress()*100)
        print(p)
        item = {'name':dl.name,'date':dl.deadline,'progress':p}
        upcoming.append(item)
    upcoming2 = [
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
