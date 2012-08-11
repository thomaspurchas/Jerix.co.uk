import datetime

from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify

from files.models import Document
from accounts.models import AuthoredObject

# Create your models here.
class Subject(models.Model):
    """(Subject description)"""

    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __unicode__(self):
        return unicode(self.title)

class AcademicYear(models.Model):
    """(AcademicYear description)"""

    title = models.CharField(max_length=50)

    def __unicode__(self):
        return unicode(self.title)

class History(models.Model):
    """(History description)"""

    title = models.CharField(max_length=50)

    start_date = models.DateField(default=datetime.datetime.today)
    end_date = models.DateField()

    class Meta:
        ordering = ['-end_date', 'start_date']

    def __unicode__(self):
        return unicode(self.title)


class HistoryMixIn(models.Model):
    """(AcademicYearMixIn description)"""

    def period_defualt():
        h = History.objects.all()
        if h:
            return h[0]
        else:
            return None

    historical_period = models.ForeignKey(History, null=True, default=period_defualt)

    def in_range(self, today):
        return (
            (historical_period is None) or
            (self.historical_period.start_date < today and
            self.historical_period.end_date > today)
        )

    def current(self):
        """docstring for current"""

        return self.in_range(datetime.datetime.today)

    class Meta:
        abstract = True

class Module(models.Model):
    """Represents a course module"""

    title = models.CharField(blank=False, max_length=100)
    short_code = models.CharField(blank=False, max_length=20)
    description = models.TextField(blank=True)
    subject = models.ForeignKey(Subject)
    year = models.ForeignKey(AcademicYear)

    lecturers = models.ManyToManyField('accounts.LecturerProfile',
                                        related_name='modules')

    class Admin:
        list_display = ('',)
        search_fields = ('',)

    def get_absolute_url(self):
        return reverse('module-posts', kwargs={"module_id": self.id,
                            "slug": slugify(self.title)})

    def __unicode__(self):
        return u'%s - %s' % (self.short_code, self.title)

class Post(AuthoredObject):
    """(BasicPost description)"""

    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    post_date = models.DateTimeField(default=datetime.datetime.now)

    def sorted_materials(self):
        return self.materials.order_by('index')

    def __unicode__(self):
        try:
            name = self.parentpost
        except:
            try:
                name = self.subpost
            except:
                name = u'BasicPost'
        return unicode(name)


class ParentPost(Post, HistoryMixIn):
    """(Post description)"""

    module = models.ForeignKey(Module, related_name='posts')
    index = models.IntegerField()
    is_parent = True

    class Meta:
        unique_together = ('module', 'index', 'historical_period')
        ordering = ['module', 'index']

    def get_absolute_url(self):
        module_url = self.module.get_absolute_url()
        return "%s#%d-%s" % (module_url, self.id, slugify(self.title))

    def __unicode__(self):
        return u"%s - %s" % (self.module.title, self.title)

class SubPost(Post):
    """(SubPost description)"""

    parent = models.ForeignKey(ParentPost, related_name='sub_posts')
    index = models.IntegerField()
    is_parent = False

    class Meta:
        unique_together = ('parent', 'index')
        ordering = ['parent', 'index']

    def get_absolute_url(self):
        module_url = self.parent.module.get_absolute_url()
        return "%s#%d%d-%s" % (module_url, self.parent.id, self.id,
                                                    slugify(self.title))

    def __unicode__(self):
        return u"%s - %s - %s" % (
            self.parent.module.title,
            self.parent.title,
            self.title
        )

class Material(AuthoredObject):
    """Represents a lecture"""

    title = models.CharField(blank=False, max_length=100)
    index = models.IntegerField(blank=False, null=False)

    post = models.ForeignKey(Post, related_name='materials')

    document = models.ForeignKey('files.Document')

    @property
    def file(self):
        return self.document.file

    class Meta:
        unique_together = ('index', 'post')
        ordering = ['index']

    def __unicode__(self):
        return unicode(self.title)