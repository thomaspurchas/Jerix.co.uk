from django.db import models
from django.contrib.auth.models import User, SiteProfileNotAvailable
from django.db.models.signals import post_save

# Create your models here.
class StudentProfile(models.Model):
    """(StudentProfile description)"""

    year = models.ForeignKey('students.Year')
    tutor = models.ForeignKey('accounts.LecturerProfile')

    modules = models.ManyToManyField('modules.Module', related_name='students')

    class Admin:
        list_display = ('',)
        search_fields = ('',)

    def __unicode__(self):
        try:
            name = self.userprofile.user.username
        except:
            name = u"StudentProfile"
        return name


class LecturerProfile(models.Model):
    """(LectureProfile description)"""

    modules = models.ManyToManyField('modules.Module', related_name='lecturers',
                                        blank=True, null=True)

    class Admin:
        list_display = ('',)
        search_fields = ('',)

    def __unicode__(self):
        try:
            name = self.userprofile.user.username
        except:
            name = u"LecturerProfile"
        return name


class UserProfile(models.Model):
    """Represents a user"""

    user = models.OneToOneField(User)

    title = models.CharField(blank=True, max_length=30)
    about_me = models.TextField(blank=True)
    picture = models.ImageField(upload_to="profile_pics:", null=True, blank=True)

    lecturer_profile = models.OneToOneField(LecturerProfile, null=True, blank=True)
    student_profile = models.OneToOneField(StudentProfile, null=True, blank=True)

    current_reputation = models.IntegerField(default=0)

    def full_name(self):
        """docstring for full_name"""

        return u'%s %s' % (self.user.first_name, self.user.last_name)

    def full_title(self):
        """docstring for full_title"""

        return u'%s %s' % (self.title, self.full_name())

    def is_lecturer(self):
        return True if self.lecturer_profile else False

    def is_student(self):
        return True if self.student_profile else False

    class Admin:
        list_display = ('',)
        search_fields = ('',)

    def __unicode__(self):
        return unicode(self.user.username)

class AuthoredObject(models.Model):
    """(AuthoredObject description)"""

    author = models.ForeignKey(User, related_name="+")

    def author_full_name(self):
        """docstring for full_name"""

        name = u'%s %s' % (self.author.first_name, self.author.last_name)

        if name.strip() == u"":
            name = self.author.username

        return name

    def author_full_title(self):
        """docstring for author_full_title"""

        name = self.author.get_profile().full_title()

        if name.strip() == u"":
            name = self.author.username

        return name

    class Meta:
        abstract = True

    class Admin:
        list_display = ('',)
        search_fields = ('',)

    def __unicode__(self):
        return u"AuthoredObject"


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)