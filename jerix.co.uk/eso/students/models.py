from django.db import models

# Create your models here.
class Year(models.Model):
    """(Year description)"""

    title = models.CharField(max_length=30)

    description = models.TextField(blank=True)

    def __unicode__(self):
        return unicode(self.title)
