from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
import datetime

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

# **************** ASSESSMENT ************************

def edit_assessment_name(request, id=None):
    if request.method == 'POST':
        name = request.POST['name']
        if name == '':
            return HttpResponse("You must write a name for the assessment.",status=400)
        assessment=Assessment.objects.get(pk=id)
        assessment.name = name
        assessment.save()

        return HttpResponse('')

def edit_assessment_description(request, id=None):
    if request.method == 'POST':
        description = request.POST['description']
        assessment=Assessment.objects.get(pk=id)
        assessment.description = description
        assessment.save()

        return HttpResponse('')

def edit_assessment_startdate(request, id=None):
    if request.method == 'POST':
        date_str = request.POST['startdate']
        date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
        assessment=Assessment.objects.get(pk=id)
        if date > assessment.deadline:
            return HttpResponse("The start date cannot be after the deadline.",status=400)
        assessment.startDate = date
        assessment.save()

        return HttpResponse('')

def edit_assessment_deadline(request, id=None):
    if request.method == 'POST':
        date_str = request.POST['deadline']
        date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
        assessment=Assessment.objects.get(pk=id)
        if date < assessment.startDate:
            return HttpResponse("The deadline date cannot be before the start date.",status=400)
        assessment.deadline = date
        assessment.save()

        return HttpResponse('')

# **************** TASK **********************

def edit_task_name(request, id=None):
    if request.method == 'POST':
        name = request.POST['name']
        if name == '':
            return HttpResponse("You must write a name for the task.",status=400)
        task=StudyTask.objects.get(pk=id)
        task.name = name
        task.save()

        return HttpResponse('')

def edit_task_description(request, id=None):
    if request.method == 'POST':
        description = request.POST['description']
        task=StudyTask.objects.get(pk=id)
        task.description = description
        task.save()

        return HttpResponse('')

def edit_task_duration(request, id=None):
    if request.method == 'POST':
        duration = request.POST['duration']
        try: 
            duration_days = int(duration)
        except ValueError:
            return HttpResponse("Invalid entry: must be a number",status=400)
        if(duration_days<=0):
            return HttpResponse("Invalid entry: must enter a number superior to zero.",status=400)
        task=StudyTask.objects.get(pk=id)
        deadline=task.assessment.deadline
        start=task.assessment.startDate
        diff=deadline-start
        if duration_days>diff.days:
            return HttpResponse("Invalid entry: The number of days must not be superior the number of days between the start date and the deadline (" + str(diff.days) + ").",status=400)
        task.duration = datetime.timedelta(days=duration_days)
        task.save()
        return HttpResponse('')

def delete_req_task(request, id=None):
    if request.method == 'POST':
        req_task_id = request.POST['task_id']
        task=StudyTask.objects.get(pk=id)
        req_task=task.requiredTasks.filter(pk=req_task_id)
        if req_task.exists():
            task.requiredTasks.remove(req_task[0])
            return HttpResponse('')
        else:
            return HttpResponse("Could not remove required task.",status=400)

def add_req_task(request, id=None):
    if request.method == 'POST':
        req_task_id = request.POST['task_id']
        task=StudyTask.objects.get(pk=id)
        req_task=task.assessment.studytask_set.filter(pk=req_task_id)
        if req_task.exists():
            task.requiredTasks.add(req_task[0])
            return HttpResponse('')
        else:
            return HttpResponse("Could not remove required task.",status=400)

def add_activity(request, id=None):
    if request.method == 'POST':
        act_name = request.POST['name']
        act_type = request.POST['type']
        act_target = request.POST['target']
        try: 
            act_target = int(act_target)
        except ValueError:
            return HttpResponse("Invalid entry: Target must be a number",status=400)
        if(act_target<=0):
            return HttpResponse("Invalid entry: Target must enter a number superior to zero.",status=400)
        if act_name == '':
            return HttpResponse("You must write a name for the activity.",status=400)
        task=StudyTask.objects.get(pk=id)
        new_act=task.studyactivity_set.create(name=act_name,target=act_target,type_act=act_type)
        data = {
            'id' : str(new_act.uid),
            'name' : new_act.name,
            'type' : new_act.get_type_act_display(),
            'task_progress' : int(task.progress()*100),
        }
        return HttpResponse(json.dumps(data), content_type="application/json")

def add_note(request, id=None):
    if request.method == 'POST':
        note_text = request.POST['note']
        if note_text == '':
            return HttpResponse("The note must not be empty.",status=400)
        task=StudyTask.objects.get(pk=id)
        new_note=task.note_set.create(notes=note_text,date=datetime.datetime.now())
        data = {
            'id' : str(new_note.uid),
            'note' : new_note.notes,
            'date' : new_note.date.strftime("%B %-d, %Y"),
        }
        return HttpResponse(json.dumps(data), content_type="application/json")

def delete_note(request, id=None):
    if request.method == 'POST':
        note_id = request.POST['note_id']
        task=StudyTask.objects.get(pk=id)
        note=task.note_set.filter(pk=note_id)
        if note.exists():
            task.note_set.remove(note[0])
            return HttpResponse('')
        else:
            return HttpResponse("Could not remove note.",status=400)