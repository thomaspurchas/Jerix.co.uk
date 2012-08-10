from haystack import indexes
from modules.models import ParentPost, SubPost, Material

class PostIndex(indexes.SearchIndex):
    text = indexes.CharField(document=True, use_template=True,
                        template_name='search/indexes/modules/post_text.txt')
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
    author = indexes.CharField(model_attr='author__get_full_name')

    def get_model(self):
        return Material
