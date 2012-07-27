import os

from django.db import models
from django.db.models.signals import post_delete, pre_delete
from django.contrib.auth.models import User
from django.conf import settings

from accounts.models import AuthoredObject

# Create your models here.
class Blob(models.Model):
    """(Blob description)"""
    file_type = models.CharField(max_length=30)
    extracted_content = models.TextField(blank=True, null=True)
    
    upload_to_url = ''
    
    def upload_to(instance, name):
        parts = instance.upload_to_url.split(':')
        if len(parts) > 1:
            path = ':'.join(parts[1:])
            cont = parts[0]
        else:
            path = ''
            cont = ''
        return "%s:%s" % (cont, os.path.join(path, name))
    
    file = models.FileField(upload_to=upload_to)
    
    class Meta:
        abstract = True

    def __unicode__(self):
        return unicode(self.file.name)

class ParentBlob(Blob):
    """(File description)"""
    upload_to_url = "%s:" % settings.PARENT_BLOBS_CONTAINER
    md5_sum = models.CharField(max_length=64, unique=True)
        
class DerivedBlob(Blob):
    """(DerivedBlob description)"""
    upload_to_url = models.CharField(max_length=100, default="UnknownDerivedBlobs:")
    md5_sum = models.CharField(max_length=64)
    
    class Meta:
        unique_together = ('upload_to_url', 'md5_sum')
    
class Document(AuthoredObject):
    title = models.CharField(max_length=200)
    file_name = models.CharField(max_length=100)
    
    blob = models.ForeignKey(ParentBlob, related_name="documents")

    def get_derived_documents_of_type(self, file_type):
        """
        Returns a `QuerySet` of derived documents.
        """
        return self.blob.derived_documents.filter(blob__file_type=file_type)

    @property
    def extracted_content(self):
        return self.file.extracted_content
        
    @property
    def file(self):
        """Return the file object"""
        return self.blob.file
    
    def __unicode__(self):
        return self.title

class DerivedDocument(models.Model):

    blob = models.ForeignKey(DerivedBlob, related_name="documents")
    index = models.IntegerField(default=0)
    derived_from = models.ForeignKey(ParentBlob,
                                        related_name="derived_documents")
            
    @property
    def file(self):
        """Return the file object"""
        return self.blob.file

    class Meta:
        unique_together = ('index', 'derived_from')
        ordering = ['derived_from', 'index']

    def __unicode__(self):
        return '%s derived from: %s' % (self.blob, 
                                        self.derived_from)

def check_blob(sender, instance, **kargs):
    """Checks to see if a blob has become orphened"""
    if instance.blob.documents.count() == 0:
        instance.blob.delete()
        
post_delete.connect(check_blob, Document)
post_delete.connect(check_blob, DerivedDocument)
                                        
def delete_file(sender, instance, **kargs):
    """Deletes the file underlying the deleted blob"""
    instance.file.delete(save=False)
    
post_delete.connect(delete_file, ParentBlob)
post_delete.connect(delete_file, DerivedBlob)