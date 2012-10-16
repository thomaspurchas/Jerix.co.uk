from haystack import indexes
from files.models import Document, DerivedDocument

class DocumentIndex(indexes.SearchIndex): #, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Document

    def index_queryset(self):
        return self.get_model().objects.all()

class DerivedDocumentIndex(indexes.SearchIndex): #, indexes.Indexable):
    text = indexes.CharField(document=True, model_attr='extracted_content')

    def get_model(self):
        return DerivedDocument

    def index_queryset(self):
        return self.get_model().objects.all()