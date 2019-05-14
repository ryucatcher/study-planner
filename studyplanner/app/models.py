import uuid
from django.db import models
from enum import Enum
from datetime import datetime,timedelta

DTFORMAT = '%d-%m-%Y'

#### MODEL ####

class User(models.Model):
    userid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.CharField(max_length=320)
    firstname = models.CharField(max_length=24)
    lastname = models.CharField(max_length=24)
    password = models.CharField(max_length=128)
    displaypic = models.CharField(max_length=128,default='display.png')
    activeSemester = models.ForeignKey("SemesterStudyProfile", on_delete=models.SET_NULL,null=True,related_name="activeSemester")
    def hasSemesterStudyProfile(self):
        semesters = SemesterStudyProfile.filter(user=self)
        if semesters.count() == 0:
            return False
        else:
            return True
    def __str__(self):
        return self.firstname + " " +self.lastname

class SemesterStudyProfile(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    year = models.IntegerField()
    semester = models.CharField(max_length=32)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def allAssessments(self):
        return Assessment.objects.filter(module__semester=self)
    def allModules(self):
        return Module.objects.filter(semester=self)
    def __str__(self):
        return self.semester

class Module(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=320)
    code = models.CharField(max_length=10)
    description = models.CharField(max_length=1000)
    semester = models.ForeignKey(SemesterStudyProfile, on_delete=models.CASCADE)
    def __str__(self):
        return self.name

class Assessment(models.Model):
    ASSESSMENT_TYPES = (
        ('EX', 'Exam'),
        ('CW', 'Coursework')
    )
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=320)
    description = models.CharField(max_length=1000)
    weight = models.IntegerField()
    startDate = models.DateField()
    deadline = models.DateField()
    #assessmentType = models.CharField(max_length=11, choices=[(tag, tag.value) for tag in AssessmentType])
    type_a = models.CharField(max_length=11, choices=ASSESSMENT_TYPES)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    def progress(self):
        #tasks = StudyTask.objects.filter(assessment=self)
        tasks = self.studytask_set.all()
        size = tasks.count()
        progress = 0.0
        for t in tasks:
            progress += t.progress()/size
        return progress
    def __str__(self):
        return self.name

class StudyTask(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=320)
    description = models.CharField(max_length=1000)
    duration = models.DurationField()
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE)
    requiredTasks = models.ManyToManyField("self", symmetrical=False)
    def progress(self):
        activities = self.studyactivity_set.all()
        size = activities.count()
        progress = 0.0
        for a in activities:
            progress += a.progress()/size
        return progress
    def __str__(self):
        return self.name

class StudyActivity(models.Model):
    ACTIVITY_TYPES = (
        ('RE', 'Reading'),
        ('WR', 'Writing'),
        ('ST', 'Studying'),
        ('PR', 'Programming')
    )
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=320)
    target = models.IntegerField()
    completed = models.IntegerField(default=0)
    type_act = models.CharField(max_length=11, choices=ACTIVITY_TYPES)
    tasks = models.ManyToManyField(StudyTask)
    def progress(self):
        return self.completed/float(self.target)
    @staticmethod
    def getActTypes():
        ACTIVITY_TYPES = (
            ('RE', 'Reading', 'pages'),
            ('WR', 'Writing', 'words'),
            ('ST', 'Studying', 'hours'),
            ('PR', 'Programming', 'requirements')
        )
        act_type_options = list()
        for t in ACTIVITY_TYPES:
            item = {'tag' : t[0], 'name' : t[1], 'units' : t[2]}
            act_type_options.append(item)
        return act_type_options
    def __str__(self):
        return self.name

class Note(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    notes = models.CharField(max_length=1000)
    date = models.DateField()
    task = models.ForeignKey(StudyTask, on_delete=models.CASCADE,null=True)
    activity = models.ForeignKey(StudyActivity, on_delete=models.CASCADE,null=True)
    def __str__(self):
        return self.notes

class Milestone(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=320)
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE)
    requiredTasks = models.ManyToManyField(StudyTask)
    def hasBeenReached(self):
        tasks = self.requiredTasks.all()
        reached = True
        if len(tasks)==0:
            reached = False
        for t in tasks:
            if t.progress()<1.0:
                reached = False
        return reached