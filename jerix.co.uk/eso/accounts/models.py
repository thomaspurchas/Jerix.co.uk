from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

# Create your models here.
class StudentProfile(models.Model):
    """(StudentProfile description)"""
    

    class Admin:
        list_display = ('',)
        search_fields = ('',)

    def __unicode__(self):
        return u"StudentProfile"

        
class LecturerProfile(models.Model):
    """(LectureProfile description)"""

    class Admin:
        list_display = ('',)
        search_fields = ('',)

    def __unicode__(self):
        return u"LecturerProfile"

class UserProfile(models.Model):
    """Represents a user"""
    
    user = models.OneToOneField(User)
    
    lecturer_profile = models.OneToOneField(LecturerProfile, null=True, blank=True, related_name='user')
    student_profile = models.OneToOneField(StudentProfile, null=True, blank=True, related_name='user')

    class Admin:
        list_display = ('',)
        search_fields = ('',)

    def __unicode__(self):
        return unicode(self.user.username)


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)