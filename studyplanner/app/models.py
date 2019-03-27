import uuid
from django.db import models
from enum import Enum

class User(models.Model):
    userid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.CharField(max_length=320)
    firstname = models.CharField(max_length=24)
    lastname = models.CharField(max_length=24)
    password = models.CharField(max_length=128)

class SemesterStudyProfile(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    year = models.IntegerField()
    semester = models.CharField(max_length=32)

class UserSemesterTable(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    semester = models.OneToOneField(SemesterStudyProfile, on_delete=models.CASCADE)

class Module(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=320)
    code = models.CharField(max_length=10)
    description = models.CharField(max_length=1000)

class SemesterModuleTable(models.Model):
    semester = models.ForeignKey(SemesterStudyProfile, on_delete=models.CASCADE)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)

class Assessment(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=320)
    description = models.CharField(max_length=1000)
    weight = models.IntegerField()
    startDate = models.DateField()
    deadline = models.DateField()
    progress = models.FloatField()

class ModuleAssessmentTable(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    assessment = models.OneToOneField(Assessment, on_delete=models.CASCADE)

class StudyTask(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=320)
    description = models.CharField(max_length=1000)
    duration = models.DurationField()
    progress = models.FloatField()

class Type(Enum):
    RE = "Reading"
    WR = "Writing"
    ST = "Studying"
    PR = "Programming"

class StudyActivity(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=320)
    target = models.IntegerField()
    progress = models.FloatField()
    actType = models.CharField(max_length=11, choices=[(tag, tag.value) for tag in Type])

class Note(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    notes = models.CharField(max_length=1000)
    date = models.DateField()

class AssessmentTaskTable(models.Model):
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE)
    task = models.OneToOneField(StudyTask, on_delete=models.CASCADE)

class TaskRequiresTaskTable(models.Model):
    task = models.ForeignKey(StudyTask, on_delete=models.CASCADE)
    requiredTask = models.ForeignKey(StudyTask, on_delete=models.CASCADE,related_name="requiredTask")

class TaskActivityTable(models.Model):
    task = models.ForeignKey(StudyTask, on_delete=models.CASCADE)
    activity = models.ForeignKey(StudyActivity, on_delete=models.CASCADE)

class TaskNoteTable(models.Model):
    task = models.ForeignKey(StudyTask, on_delete=models.CASCADE)
    note = models.OneToOneField(Note, on_delete=models.CASCADE)

class ActivityNoteTable(models.Model):
    activity = models.ForeignKey(StudyActivity, on_delete=models.CASCADE)
    note = models.OneToOneField(Note, on_delete=models.CASCADE)

class Milestone(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=320)

class MilestoneRequiresTaskTable(models.Model):
    milestone = models.ForeignKey(Milestone, on_delete=models.CASCADE)
    requiredTask = models.ForeignKey(StudyTask, on_delete=models.CASCADE)

class AssessmentMilestoneTable(models.Model):
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE)
    milestone = models.OneToOneField(Milestone, on_delete=models.CASCADE)