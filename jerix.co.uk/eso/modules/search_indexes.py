from django.template import loader, Context

from haystack import indexes

from modules.models import ParentPost, SubPost, Material

def get_content(doc, backend):
    if doc.extracted_content == None:
        file_obj = doc.file
        content = backend.extract_file_contents(file_obj)
        doc._blob.extracted_content = content
        doc._blob.save()

    return doc.extracted_content

class PostIndex(indexes.SearchIndex):
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

class MaterialIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    author = indexes.CharField(model_attr='author__get_full_name', faceted=True)
    tags = indexes.MultiValueField(faceted=True)

    def prepare_tags(self, obj):
        tags = list(obj.post.tags.all())

        if hasattr(obj.post, 'parentpost'):
            tags.append(obj.post.parentpost.module.primary_tag)
        else:
            tags.append(obj.post.subpost.parent.module.primary_tag)

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
