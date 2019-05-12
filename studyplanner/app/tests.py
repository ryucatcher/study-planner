from django.test import TestCase

# Create your tests here.

from app.models import *
from datetime import datetime, timedelta

#### UNIT TESTS ####
def run_unit_tests():
    print('Running create user test...')
    result = _ut_create_user()
    if result:
        print('Success')
    else:
        print('Test failed.')

    print('Running create assessment test...')
    result = _ut_create_assessment()
    if result:
        print('Success')
    else:
        print('Test failed.')

    print('Running create task test...')
    result = _ut_create_studytask()
    if result:
        print('Success')
    else:
        print('Test failed.')

    print('Running create milestone test...')
    result = _ut_create_milestone()
    if result:
        print('Success')
    else:
        print('Test failed.')

def _ut_create_user():
    u = User(email="usertest@gmail.com", firstname="firstname", lastname="lastname", password="testpassword")
    oldUserCount = len(User.objects.all())
    u.save()
    newUserCount = len(User.objects.all())
    success = True
    if newUserCount != oldUserCount + 1:
        print('User was not added to database.')
        success = False
    if u.email != "usertest@gmail.com" or u.firstname != "firstname" or u.lastname != "lastname" or u.password != "testpassword":
        print('User details do not match.')
        success = False
    u.delete()
    return success
    
def _ut_create_assessment():
    a = Assessment(name="unit_test", weight=40, type_a="CW", startDate=datetime.now(), deadline=datetime.now(), module=Module.objects.all()[0])
    count = len(Assessment.objects.all())
    a.save()
    success = True
    if len(Assessment.objects.all()) != count + 1:
        print('Assessment was not added to database.')
        success = False
    if a.type_a != "CW":
        print('Assessment type was not retained.')
        success = False
    a.delete()
    return success

def _ut_create_studytask():
    a = Assessment.objects.all()[0]
    t = StudyTask(name="unit_test", duration=timedelta(days=3), assessment=a)
    count = len(StudyTask.objects.all())
    t.save()
    success = True
    if len(StudyTask.objects.all()) != count + 1:
        print('StudyTask was not added to database.')
        success = False
    if t.duration.days != 3:
        print('StudyTask duration is ' + t.duration.days + '. Expected 3.')
        success = False
    t.delete()
    return success

def _ut_create_milestone():
    a = Assessment.objects.all()[0]
    count = len(Milestone.objects.all())
    milestone = a.milestone_set.create(name="unit_test")
    success = True
    if len(Milestone.objects.all()) != count + 1:
        print('Milestone was not added to database.')
        success = False
    if milestone.name != "unit_test":
        print('Milestone name was "' + milestone.name + '". Expected "unit_test"')
        success = False
    milestone.delete()
    return success