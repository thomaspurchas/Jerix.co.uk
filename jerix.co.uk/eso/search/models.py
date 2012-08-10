from django.db import models

# Create your models here.
class Tag(models.Model):
    """(Tag description)"""

    title = models.CharField(blank=False, max_length=30, unique=True)

    def __unicode__(self):
        return u"#%s" % self.title

class SmartTag(models.Model):
    """(SmartTag description)"""

    tag = models.ForeignKey(Tag)

    def _get_title(self):
        return self.tag.title

    def _set_title(self, value):
        self.tag.title = value

    title = property(_get_title, _set_title)

    class Meta:
        abstract = True

    def __unicode__(self):
        return u"SmartTag"

class TagableObject(models.Model):
    """(TagableObject description)"""

    tags = models.ManyToManyField(Tag, related_name="+")

    class Meta:
        abstract = True

    def __unicode__(self):
        return u"TagableObject"
