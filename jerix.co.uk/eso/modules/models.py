import datetime

from django.db import models
from django.contrib.auth.models import User

from accounts.models import AuthoredObject

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


class ParentPost(Post):
    """(Post description)"""

    module = models.ForeignKey(Module, related_name='posts')
    index = models.IntegerField()

    class Meta:
        unique_together = ('module', 'index')
        ordering = ['index']

    def __unicode__(self):
        return u"%s - %s" % (self.module.title, self.title)

class SubPost(Post):
    """(SubPost description)"""

    parent = models.ForeignKey(ParentPost, related_name='sub_posts')
    index = models.IntegerField()

    class Meta:
        unique_together = ('parent', 'index')
        ordering = ['parent', 'index']

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

    #file = models.ForeignKey(RELATED_MODEL)

    class Meta:
        unique_together = ('index', 'post')
        ordering = ['index']

    def __unicode__(self):
        return unicode(self.title)