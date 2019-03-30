from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
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


def login(request):
    # If user already logged in
    if 'userid' in request.COOKIES:
        return redirect('/dashboard')
    
    # error context
    context = {}
    if 'error' in request.GET:
        context['error'] = request.GET['error']

    return render(request,'login.html', context)

def isValidEmail(email):
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False

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
    response.set_cookie('userid', user.userid)

    return response
def dashboard(request):
    context = {
        'navigation': navigation_list,
        'active': 'Deadlines',
        'csrf': csrf.get_token(request)
    }
    return render(request, 'dashboardtest.html', context)

def uploadHubFile(request):

    return redirect('/dashboard')
