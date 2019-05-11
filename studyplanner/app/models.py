import uuid
from django.db import models
from enum import Enum

DTFORMAT = '%d-%m-%Y'

#### UNIT TESTS #####
def run_unit_tests():
    print('Running create user test...')
    result = _ut_create_user()
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


class User(models.Model):
    userid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.CharField(max_length=320)
    firstname = models.CharField(max_length=24)
    lastname = models.CharField(max_length=24)
    password = models.CharField(max_length=128)
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

#class AssessmentType(Enum):
#    EX = "Exam"
#    CW = "Coursework"

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
    requiredTasks = models.ManyToManyField("self")
    def progress(self):
        activities = self.studyactivity_set.all()
        size = activities.count()
        progress = 0.0
        for a in activities:
            progress += a.progress()/size
        return progress
    def __str__(self):
        return self.name

#class Type(Enum):
#    RE = "Reading"
#    WR = "Writing"
#    ST = "Studying"
#    PR = "Programming"

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

#class UserSemesterTable(models.Model):
#    user = models.ForeignKey(User, on_delete=models.CASCADE)
#    semester = models.OneToOneField(SemesterStudyProfile, on_delete=models.CASCADE)

#class SemesterModuleTable(models.Model):
#    semester = models.ForeignKey(SemesterStudyProfile, on_delete=models.CASCADE)
#    module = models.ForeignKey(Module, on_delete=models.CASCADE)

#class AssessmentTaskTable(models.Model):
#    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE)
#    task = models.OneToOneField(StudyTask, on_delete=models.CASCADE)

#class TaskRequiresTaskTable(models.Model):
#    task = models.ForeignKey(StudyTask, on_delete=models.CASCADE)
#    requiredTask = models.ForeignKey(StudyTask, on_delete=models.CASCADE,related_name="requiredTask")

#class TaskActivityTable(models.Model):
#    task = models.ForeignKey(StudyTask, on_delete=models.CASCADE)
#    activity = models.ForeignKey(StudyActivity, on_delete=models.CASCADE)

#class TaskNoteTable(models.Model):
#    task = models.ForeignKey(StudyTask, on_delete=models.CASCADE)
#    note = models.OneToOneField(Note, on_delete=models.CASCADE)

#class ActivityNoteTable(models.Model):
#    activity = models.ForeignKey(StudyActivity, on_delete=models.CASCADE)
#    note = models.OneToOneField(Note, on_delete=models.CASCADE)

#class MilestoneRequiresTaskTable(models.Model):
#    milestone = models.ForeignKey(Milestone, on_delete=models.CASCADE)
#    requiredTask = models.ForeignKey(StudyTask, on_delete=models.CASCADE)

#class AssessmentMilestoneTable(models.Model):
#    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE)
#    milestone = models.OneToOneField(Milestone, on_delete=models.CASCADE)

#class ModuleAssessmentTable(models.Model):
#    module = models.ForeignKey(Module, on_delete=models.CASCADE)
#    assessment = models.OneToOneField(Assessment, on_delete=models.CASCADE)