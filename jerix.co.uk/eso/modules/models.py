import datetime

from django.db import models
from users.models import User

# Create your models here.
class Module(models.Model):
    """Represents a course module"""
    
    Title = models.TextField(blank=False)
    ShortCode = models.TextField(blank=False)
    Description = models.TextField(blank=True)
    
    Lecturers = models.ManyToManyField(User)

    class Admin:
        list_display = ('',)
        search_fields = ('',)

    def __unicode__(self):
        return unicode(self.Title)

class Lecture(models.Model):
    """Represents a lecture"""
    
    Title = models.TextField(blank=False)
    Index = models.IntegerField(blank=False, null=False)
    
    PresentationDate = models.DateTimeField(blank=False, default=datetime.datetime.now)

    class Admin:
        list_display = ('',)
        search_fields = ('',)

    def __unicode__(self):
        return unicode(self.Title)
