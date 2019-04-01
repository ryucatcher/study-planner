from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

import json

# Create your views here.
from .models import User

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
    errorMsg = []
    result = {}
    try:
        config = json.loads(request.body)
        
        # Get user from userid
        # If user doesn't exist, return error
        try:
            user = User.objects.get(userid=config.userid)
        except:
            errorMsg.append('User with this ID does not exist.')
            raise Exception()
        
        # Get semester year
        try:
            year = config.year
        except:
            errorMsg.append('Year attribute was not found.')
            raise Exception()

        # Try to find semester
        try:
            profile = SemesterStudyProfile.objects.get(year=year, user=user)
            result = profile
            result['modules'] = []
        except:
            errorMsg.append('Could not find semester study profile.')
            raise Exception()

        # Retrieve modules
        modules = Module.objects.filter(semester=profile)
        
        for m in modules:
            module = m
            module['assessments'] = []
            # Find assessments
            assessments = Assessment.objects.filter(module=m)
            for a in assessments:
                assessment = a
                assessment['tasks'] = []
                # Find tasks
                assessment.tasks = StudyTask.objects.filter(assessment=a)
                # Append assessment
                module.assessments.append(assessment)
            # Append module
            profile.modules.append(module)
        
        # Return study profile as json
        return HttpResponse(json.dumps(profile))

    except:
        response_data = {'error': errorMsg}
        return HttpResponse(json.dumps(response_data))