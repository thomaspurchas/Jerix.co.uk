from django.db import models

# Create your models here.
class User(models.Model):
    """Represents a user"""
    

    class Admin:
        list_display = ('',)
        search_fields = ('',)

    def __unicode__(self):
        return u"User"
