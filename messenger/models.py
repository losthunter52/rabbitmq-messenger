from django.db import models
from datetime import datetime

# Create your models here.
class Contact(models.Model):
    name = models.CharField(max_length=32, unique=True, default='')

class ContactMessage(models.Model):
    message = models.CharField(max_length=256)
    date = models.DateTimeField(default=datetime.now, blank=True)
    origin = models.CharField(max_length=32, default='')
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)

class Group(models.Model):
    name = models.CharField(max_length=32, default='Group')
    group = models.CharField(max_length=32, unique=True, default='')

class GroupMessage(models.Model):
    message = models.CharField(max_length=256)
    date = models.DateTimeField(default=datetime.now, blank=True)
    origin = models.CharField(max_length=32, default='')
    group = models.ForeignKey(Group, on_delete=models.CASCADE)