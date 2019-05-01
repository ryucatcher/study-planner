from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

import json

# Create your views here.
from .models import *

def updateDeadlineName(request):
    postdata = json.loads(request.body)

    return_value = {
        'status': 'ok'
    }
    return HttpResponse(json.dumps(return_value))

def updateTaskProgress(request):
    postdata = json.loads(request.body)

    return_value = {
        'status': 'ok'
    }
    return HttpResponse(json.dumps(return_value))

def getUserStudyProfile(request):
    result = {
        'error': []
    }
    try:
        config = json.loads(request.body)
        
        # Get user from userid
        # If user doesn't exist, return error
        try:
            user = User.objects.get(userid=config['userid'])
            result['user'] = {
                'email': user.email,
                'firstname': user.firstname,
                'lastname': user.lastname
            }
        except Exception as e:
            print(e)
            result['error'].append('User with this ID does not exist.')
            raise Exception()
        
        # Get semester year
        try:
            year = config['year']
        except:
            result['error'].append('Year attribute was not found.')
            raise Exception()

        # Try to find semester
        try:
            profile = SemesterStudyProfile.objects.get(year=year, user=user)
            result['year'] = profile.year
            result['semester'] = profile.semester
            result['modules'] = []
        except Exception as e:
            print(e)
            result['error'].append('Could not find semester study profile.')
            raise Exception()

        # Retrieve modules
        modules = Module.objects.filter(semester=profile)
        
        for m in modules:
            module = {
                'name': m.name,
                'code': m.code,
                'description': m.description,
                'assessments': []
            }
            # Find assessments
            assessments = Assessment.objects.filter(module=m)
            for a in assessments:
                assessment = {
                    'name': a.name,
                    'weight': a.weight,
                    'description': a.description,
                    'startdate': a.startDate.strftime(DTFORMAT),
                    'deadline': a.deadline.strftime(DTFORMAT),
                    'assessmentType': a.assessmentType,
                    'tasks': []
                }
                # Find tasks
                tasks = StudyTask.objects.filter(assessment=a)
                for t in tasks:
                    task = {
                        'name':  t.name,
                        'description': t.description,
                        'duration': t.duration,
                        'dependencies': []
                    }
                    for d in t.requiredTasks():
                        task['dependencies'].append(d.uid)
                    assessment['tasks'].append(task)
                # Append assessment
                module['assessments'].append(assessment)
            # Append module
            result['modules'].append(module)
        
        # Return study profile as json
        return HttpResponse(json.dumps(result))

    except Exception as e:
        print(e)
        return HttpResponse(json.dumps(result))