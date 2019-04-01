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
from datetime import date,timedelta

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
    if not isLoggedIn(request):
        return redirect('/')
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
    today = date.today()
    u = User.objects.all()[0]
    s = u.activeSemester
    deadlines = s.allAssessments().order_by('deadline')
    upcoming = list()
    inprogress = list()
    missed = list()
    completed = list()
    for dl in deadlines:
        deadline = dl.deadline
        progress = dl.progress()
        p = int(progress*100)
        item = {'name':dl.name,'date':deadline,'progress':p,'id':dl.uid}

        diff_date = deadline - today
        diff_days = diff_date.days
        # Deadline has passed and has not been completed yet -> missed
        if deadline < today and progress<1.0:
            missed.append(item)
        # Progress is 100% -> completed
        if progress==1.0:
            completed.append(item)
        # Progress is more than 0%, but less than 100% -> in progress
        if progress>0.0 and progress<1.0:
            inprogress.append(item)
        # Deadline hasn't passed yet -> upcoming
        if not(deadline < today):
            # If deadline is in less than a month it will always be added to upcoming
            # If it is further away, it will be added is there are less than 4 deadlines
            # so far on the list (to avoid overwhelming)
            if diff_days<31 or len(upcoming)<4:
                upcoming.append(item)
    completed.reverse() #showing the most recent completed first
    context = {
        'navigation': navigation_list,
        'active': 'Deadlines',
        'upcoming' : upcoming,
        'inprogress' : inprogress,
        'missed' : missed,
        'completed' : completed
    }
    return render(request, 'deadlines.html', context)

def assessment(request, id=None):
    assessment=Assessment.objects.get(pk=id)
    tasks = list()
    for t in assessment.studytask_set.all():
        p = int(t.progress()*100)
        item = {'name' : t.name, 'progress' : p, 'id' : t.uid }
        tasks.append(item)
    progress = int(assessment.progress()*100)
    assessment = {
        'name' : assessment.name,
        'type' : assessment.get_type_a_display(),
        'module' : assessment.module.name,
        'module_id' : assessment.module.uid,
        'startdate' : assessment.startDate,
        'deadline' : assessment.deadline,
        'weight' : assessment.weight,
        'description' : assessment.description,
        'progress' : progress,
        'tasks' : tasks
    }
    context = {
        'navigation': navigation_list,
        'active': 'Deadlines',
        'assessment' : assessment
    }
    return render(request, 'assessment.html', context)

def task(request, id=None):
    task=StudyTask.objects.get(pk=id)
    activities = list()
    notes = list()
    requiredTasks = list()
    for a in task.studyactivity_set.all():
        p = int(a.progress()*100)
        item = {'name' : a.name, 'type' : a.get_type_act_display(),
            'progress' : p, 'id' : a.uid
        }
        activities.append(item)
    for n in task.note_set.all():
        p = int(a.progress()*100)
        item = {'note' : n.notes, 'date' : n.date, 'id' : n.uid }
        notes.append(item)
    for t in task.requiredTasks.all():
        item = {'name' : t.name, 'id' : t.uid }
        requiredTasks.append(item)
    progress = int(task.progress()*100)
    task = {
        'name' : task.name,
        'assessment' : task.assessment,
        'duration' : task.duration.days,
        'description' : task.description,
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
