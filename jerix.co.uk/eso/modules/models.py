import datetime

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Module(models.Model):
    """Represents a course module"""

    title = models.CharField(blank=False, max_length=100)
    short_code = models.CharField(blank=False, max_length=20)
    description = models.TextField(blank=True)

    lecturers = models.ManyToManyField(User)

    class Admin:
        list_display = ('',)
        search_fields = ('',)

    def __unicode__(self):
        return unicode(self.title)

class Lecture(models.Model):
    """Represents a lecture"""

    title = models.CharField(blank=False, max_length=100)
    index = models.IntegerField(blank=False, null=False)
    module = models.ForeignKey(Module, related_name='lectures')

    presentation_datetime = models.DateTimeField(blank=False, default=datetime.datetime.now)
    lecturer = models.ForeignKey(User)

    class Admin:
        list_display = ('',)
        search_fields = ('',)

    def __unicode__(self):
        return unicode(self.title)