import datetime

from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify
from django.db.models.signals import pre_save

from taggit.managers import TaggableManager
from taggit.models import Tag

from files.models import Document
from accounts.models import AuthoredObject

# Create your models here.
class Subject(models.Model):
    """(Subject description)"""

    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    primary_tag = models.ForeignKey(Tag, related_name='+')
    tags = TaggableManager(blank=True)

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
    short_code = models.CharField(blank=False, max_length=20, unique=True)
    description = models.TextField(blank=True)
    subject = models.ForeignKey(Subject)
    year = models.ForeignKey(AcademicYear, related_name="modules")
    primary_tag = models.ForeignKey(Tag, related_name='+')
    tags = TaggableManager(blank=True)
    source_url = models.URLField(blank=True)
    
    # There is a lectures manytomany relation on the lecture profile module.

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

    @property
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
    tags = TaggableManager(blank=True)
    is_parent = True

    class Meta:
        unique_together = ('module', 'index', 'historical_period')
        ordering = ['module', 'index']

    @property
    def slug(self):
        return u"%d-%s" % (self.post_ptr.id, slugify(self.title))

    def get_absolute_url(self):
        module_url = self.module.get_absolute_url()
        return u"%s#" % (module_url, self.slug)

    def __unicode__(self):
        return u"%s - %s" % (self.module.title, self.title)

class SubPost(Post):
    """(SubPost description)"""

    parent = models.ForeignKey(ParentPost, related_name='sub_posts')
    index = models.IntegerField()
    tags = TaggableManager(blank=True)
    is_parent = False

    class Meta:
        unique_together = ('parent', 'index')
        ordering = ['parent', 'index']

    @property
    def slug(self):
        return u"%d-%s" %(self.post_ptr.id, slugify(self.title))

    def get_absolute_url(self):
        module_url = self.parent.module.get_absolute_url()
        return u"%s#%s" % (module_url, self.slug)

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

    template = 'material.html'

    @property
    def file(self):
        return self.document.file

    class Meta:
        unique_together = ('index', 'post')
        ordering = ['index']

    def __unicode__(self):
        return u"%s - %s" % (self.post, self.title)

def primary_tag_changed(instance):
    klass = instance.__class__
    if instance.id:
        old_instance = klass.objects.get(pk=instance.pk)
        if old_instance.primary_tag != instance.primary_tag:
            return old_instance.primary_tag
        return False
    else:
        return None

def add_parent_primary_to_tags(sender, instance, raw, **kwargs):
    if raw:
        return

    if isinstance(sender, ParentPost):
        parents = [instance.module, instance.module.subject]

    elif isinstance(sender, SubPost):
        parents = [instance.parent.module, instance.parent.module.subject]

    remove = []
    add = []
    old_tag = primary_tag_changed(Module, parents[0])
    if old_tag:
        remove.append(old_tag)
        add.append(parents[0].primary_tag)
    old_tag = primary_tag_changed(Module, parents[0])
    if old_tag:
        remove.append(old_tag)
        add.append(parents[1].primary_tag)

    self.tags.remove(remove)
    self.tags.add(add)