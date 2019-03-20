from django.db import models

class User(models.Model):
    userid = models.UUIDField(primary_key=True, editable=False)
    email = models.CharField(max_length=320)
    firstname = models.CharField(max_length=24)
    lastname = models.CharField(max_length=24)
    password = models.CharField()