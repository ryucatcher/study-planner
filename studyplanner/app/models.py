import uuid
from django.db import models

class User(models.Model):
    userid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.CharField(max_length=320)
    firstname = models.CharField(max_length=24)
    lastname = models.CharField(max_length=24)
    password = models.CharField(max_length=128)

class SemesterStudyProfile(models.Model):
    uid = models.UUIDField(primary_key=True, editable=False)
    year = models.IntegerField()
    semester = models.CharField(max_length=32)

class UserSemesterTable(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    semester = models.ForeignKey(SemesterStudyProfile, on_delete=models.CASCADE)
