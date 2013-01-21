import logging

from django.template import loader, Context
from django.db.models import signals

from haystack import indexes
from celery_haystack.indexes import CelerySearchIndex
from pysolr import SolrError

from modules.models import ParentPost, SubPost, Material
from files.models import DerivedDocument

log = logging.getLogger(__name__)

def get_content(doc, backend):
    if doc.extracted_content == None:
        file_obj = doc.file
        file_obj.seek(0)
        try:
            content = backend.extract_file_contents(file_obj)
            # Note: This may return None if it can't connect to the search
            # server.
            doc.extracted_content = content
            doc.save()
        except SolrError as e:
            content = ""
            if not doc.extraction_error:
                msg = ('Extracting content from: %s resulted in the ' +
                         'following pysolr error:\n%s')
                log.error( msg % (doc._blob, e))
                doc.extraction_error = True
                doc.save()
        else:
            if doc.extraction_error == True:
                doc.extraction_error = False
                doc.save()
    else:
        content = doc.extracted_content

    return content

class PostIndex(CelerySearchIndex):
    text = indexes.CharField(document=True, use_template=True)
    author = indexes.CharField(model_attr='author__get_full_name')

    def index_queryset(self):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()

class ParentPostIndex(PostIndex, indexes.Indexable):

    def get_model(self):
        return ParentPost

class SubPostIndex(PostIndex, indexes.Indexable):

    def get_model(self):
        return SubPost

class MaterialIndex(CelerySearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    author = indexes.CharField(model_attr='author__get_full_name', faceted=True)
    tags = indexes.MultiValueField(faceted=True)

    def prepare_tags(self, obj):
        if hasattr(obj.post, 'parentpost'):
            post = obj.post.parentpost
            module = obj.post.parentpost.module
        elif hasattr(obj.post, 'subpost'):
            post = obj.post.subpost
            module = obj.post.subpost.parent.module

        tags = list(post.tags.all())
        tags.append(module.primary_tag)

        return tags

    def prepare_text(self, obj):
        content = get_content(obj.document, self._get_backend(None))
        max_len = len(content)

        for doc in obj.document._blob.derived_documents.all():
            temp_content = get_content(doc, self._get_backend(None))
            length = len(temp_content)
            if length > max_len:
                content = temp_content
                max_len = length

        t = loader.select_template(('search/indexes/modules/material_text.txt',))
        return t.render(Context({'object': obj, 'extracted': content}))

    def get_model(self):
        return Material

    def index_queryset(self):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()

    def new_derived_doc(self, instance, **kwargs):
        mats = Material.objects.filter(
                    document___blob__derived_documents__pk=instance.pk)

        for mat in mats:
            self.enqueue_save(mat, **kwargs)

    def _setup_save(self):
        super(MaterialIndex, self)._setup_save()
        signals.post_save.connect(self.new_derived_doc, sender=DerivedDocument)

    def _teardown_save(self):
        super(MaterialIndex, self)._teardown_save()
        signals.post_save.disconnect(self.new_derived_doc, sender=DerivedDocument)