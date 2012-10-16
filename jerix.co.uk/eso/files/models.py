import os

from django.db import models
from django.db.models.signals import post_delete, pre_save, post_save
from django.contrib.auth.models import User
from django.conf import settings
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify

from accounts.models import AuthoredObject

from files.helpers import (identify_and_md5, generate_md5, get_path,
                           ReadOnlyFile, type_to_display, type_to_priorty)
from files.errors import ReadOnlyFileError

# Create your models here.
class Blob(models.Model):
    """(Blob description)"""
    file_type = models.CharField(max_length=30)
    extracted_content = models.TextField(blank=True, null=True)

    upload_to_url = ''

    def upload_to(instance, name):
        # This is the old version that was used for rackspace cloud.
        # As S3 supports folders, and does not have issues with a large number
        # of files in a single bucket this stuff is no longer relevant.
        # parts = instance.upload_to_url.split(':')
        # if len(parts) > 1:
        #     path = ':'.join(parts[1:])
        #     cont = parts[0]
        # else:
        #     path = ''
        #     cont = ''
        # return "%s:%s" % (cont, os.path.join(path, name))
        return os.path.join(instance.upload_to_url, name)

    file = models.FileField(upload_to=upload_to)

    @classmethod
    def blob_saved(self, sender, instance, **kargs):
        """Make sure that blob changes dont break things"""
        if instance.md5_sum in [None, '']:
            instance.file.seek(0)
            instance.md5_sum = generate_md5(instance.file)
            instance.file.seek(0)

    @classmethod
    def check_blob(cls, blob):
        """Check if the blob is orphaned"""
        if blob.documents.count() == 0:
            blob.delete()

    @classmethod
    def delete_file(cls, sender, instance, **kargs):
        """Deletes the file underlying the deleted blob"""
        if instance.file.name:
            instance.file.delete(save=False)

    class Meta:
        abstract = True

    def __unicode__(self):
        return unicode(self.file.name)

class ParentBlob(Blob):
    """(File description)"""
    upload_to_url = "%s" % settings.PARENT_BLOBS_LOCATION
    md5_sum = models.CharField(max_length=64, unique=True)

class DerivedBlob(Blob):
    """(DerivedBlob description)"""
    upload_to_url = models.CharField(max_length=100, default="UnknownDerivedBlobs/")
    md5_sum = models.CharField(max_length=64)

    class Meta:
        unique_together = ('upload_to_url', 'md5_sum')

class BaseDocument(models.Model):
    """Contains a bunch of useful functions"""

    @classmethod
    def document_saved(cls, sender, instance, raw=False, **kargs):
        """Checks changes to the document, and how they may affect underlying blobs"""
        if not raw:
            if instance._blob.id == None:
                instance._blob.save()
                # We need to do this or django goes nuts
                instance._blob = instance._blob

    @classmethod
    def document_post_save(cls, sender, instance, raw=False, **kargs):
        """Blob check needs to happen after db modification"""
        if not raw:
            if hasattr(instance, '_old_blob'):
                Blob.check_blob(instance._old_blob)
                del instance._old_blob

    @classmethod
    def document_deleted(cls, sender, instance, **kargs):
        Blob.check_blob(instance._blob)

    @property
    def type_display(self):
        return type_to_display(self.type)

    @property
    def type(self):
        return self._blob.file_type

    def _get_file(self):
        """Return the file object"""
        file = ReadOnlyFile(self._blob.file)
        return file

    class Meta:
        abstract = True

    def __unicode__(self):
        return u"BaseDocument"


class Document(BaseDocument, AuthoredObject):
    title = models.CharField(max_length=200)
    file_name = models.CharField(max_length=100)

    _blob = models.ForeignKey(ParentBlob, related_name="documents")

    def get_derived_documents_of_type(self, file_type):
        """
        Returns a `QuerySet` of derived documents.
        """
        return self._blob.derived_documents.filter(
                                            _blob__file_type=file_type)

    @property
    def versions(self):
        versions = list(self._blob.derived_documents.all())
        versions.append(self)
        for version in versions:
            version.original_document = self
            version.priority = type_to_priorty(version.type)
        return sorted(versions, key=lambda doc:doc.priority, reverse=True)

    @property
    def extracted_content(self):
        return self.file.extracted_content

    @property
    def url(self):
        """Get a public url for the file"""
        filename, ext = os.path.splitext(self.file_name)

        return reverse('download-original',
                kwargs={
                    'id': self.id,
                    'slug': "%s%s" % (slugify(filename), ext)
                })

    def _set_file(self, file):
        file_type, md5 = identify_and_md5(file)
        path = get_path(file_type)
        try:
            blob = ParentBlob.objects.get(md5_sum=md5)
        except ParentBlob.DoesNotExist:
            blob = ParentBlob(md5_sum=md5, file_type=file_type, file=file)
        if self._blob_id:
            self._old_blob = self._blob
        self._blob = blob

    file = property(BaseDocument._get_file, _set_file)

    def __unicode__(self):
        return self.title

class DerivedDocument(BaseDocument):

    _blob = models.ForeignKey(DerivedBlob, related_name="documents")
    index = models.IntegerField(default=0)
    derived_from = models.ForeignKey(ParentBlob,
                                        related_name="derived_documents")

    def _set_file(self, file):
        file_type, md5 = identify_and_md5(file)
        path = get_path(file_type)
        try:
            blob = DerivedBlob.objects.get(md5_sum=md5,
                                            upload_to_url=path)
            self._old_blob = self._blob
        except DerivedBlob.DoesNotExist:
            blob = DerivedBlob(upload_to_url=path, md5_sum=md5,
                                file_type=file_type, file=file)
        self._blob = blob

    @property
    def url(self):

        filename = os.path.basename(self.file.name)

        if hasattr(self, 'original_document'):
            ext = os.path.splitext(filename)[1]
            filename = os.path.splitext(self.original_document.file_name)[0]
            orig_id = self.original_document.id
        else:
            filename, ext = os.path.splitext(filename)
            orig_id = None

        kwargs = {
            'id': self.id,
            'slug': '%s%s' % (slugify(filename), ext),
        }

        if orig_id:
            kwargs['orig_id'] = orig_id
            return reverse('download-derived-with-orig', kwargs=kwargs)
        else:
            return reverse('download-derived', kwargs=kwargs)

    file = property(BaseDocument._get_file, _set_file)

    class Meta:
        unique_together = ('index', 'derived_from')
        ordering = ['derived_from', 'index']

    def __unicode__(self):
        return '%s derived from: %s' % (self._blob,
                                        self.derived_from)

pre_save.connect(BaseDocument.document_saved, Document)
pre_save.connect(BaseDocument.document_saved, DerivedDocument)

post_save.connect(BaseDocument.document_post_save, Document)
post_save.connect(BaseDocument.document_post_save, DerivedDocument)

post_delete.connect(BaseDocument.document_deleted, Document)
post_delete.connect(BaseDocument.document_deleted, DerivedDocument)

pre_save.connect(Blob.blob_saved, ParentBlob)
pre_save.connect(Blob.blob_saved, DerivedBlob)

post_delete.connect(Blob.delete_file, ParentBlob)
post_delete.connect(Blob.delete_file, DerivedBlob)