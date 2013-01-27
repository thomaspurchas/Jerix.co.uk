from django.db import models

# Create your models here.
class Year(models.Model):
    """(Year description)"""

    title = models.CharField(max_length=30)
    short_code = models.CharField(blank=False, max_length=20)

    description = models.TextField(blank=True)

    def __unicode__(self):
        return unicode(self.title)
