"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User

from files.models import Document, DerivedDocument, ParentBlob, DerivedBlob
from files.test_helpers import uploaded_new_document, uploaded_new_derived_document

class SimpleTest(TestCase):
    def setUp(self):
        self.u1 = User.objects.create(username='user1')
        self.upload = SimpleUploadedFile('fake.pdf', 'This is a fake pdf')
        self.upload2 = SimpleUploadedFile('fake2.pdf', 'This is a second fake pdf')

    def test_document_upload(self):
        """
        Tests that we can upload a file and get it back
        """
        doc = uploaded_new_document(self.upload)
        doc.title = 'File uploaded'
        doc.author = self.u1
        doc.file.read()
        doc.save()

        doc = Document.objects.get(title='File uploaded')
        self.upload.seek(0)
        self.assertEqual(doc.file.read(), self.upload.read())

    def test_derived_document_upload(self):
        """
        Test derived file upload
        """
        doc = uploaded_new_document(self.upload)
        doc.title = 'File uploaded'
        doc.author = self.u1
        doc.save()

        derived = uploaded_new_derived_document(self.upload2)
        derived.derived_from = doc._blob
        derived.index = 0
        derived.save()

        derived2 = doc.get_derived_documents_of_type('pdf')[0]
        self.assertEqual(derived, derived2)
        self.upload2.seek(0)
        self.assertEqual(derived2.file.read(), self.upload2.read())

    def test_png_container(self):

        doc = uploaded_new_document(self.upload)
        doc.title = 'File uploaded'
        doc.author = self.u1
        doc.save()

        self.upload.name = 'fake.png'
        derived = uploaded_new_derived_document(self.upload)
        derived.derived_from = doc._blob
        derived.index = 0
        derived.save()

    def test_orphaned_blobs(self):
        """Make sure that deleting a Document does not result in orphanded blobs"""
        doc = uploaded_new_document(self.upload)
        doc.title = 'File uploaded'
        doc.author = self.u1
        doc.save()

        self.upload.name = 'fake.png'
        derived = uploaded_new_derived_document(self.upload)
        derived.derived_from = doc._blob
        derived.index = 0
        derived.save()

        DerivedDocument.objects.all().delete()
        self.assertEqual(DerivedBlob.objects.count(), 0)

        Document.objects.all().delete()
        self.assertEqual(ParentBlob.objects.count(), 0)

    def test_deleted_derived(self):
        """
        Make sure that derived documents are deleted when parent document and
        blob are deleted.
        """
        doc = uploaded_new_document(self.upload)
        doc.title = 'File uploaded'
        doc.author = self.u1
        doc.save()

        self.upload.name = 'fake.png'
        derived = uploaded_new_derived_document(self.upload)
        derived.derived_from = doc._blob
        derived.index = 0
        derived.save()

        Document.objects.all().delete()
        self.assertEqual(DerivedBlob.objects.count(), 0)

    def test_files_are_deleted(self):
        """Make sure file is deleted when blob is"""
        doc = uploaded_new_document(self.upload)
        doc.title = 'File uploaded'
        doc.author = self.u1
        doc.save()
        name = doc._blob.file.name

        from django.core.files.storage import get_storage_class
        storage = get_storage_class()()

        doc.delete()
        self.assertFalse(storage.exists(name))

    def test_auto_blob_creation(self):
        """
        Test that a blob is created when using file attriube on a document.
        """
        doc = Document(title='New Doc', file_name='A File', file=self.upload,
                                                                author=self.u1)
        doc.save()
        doc.file.seek(0)
        self.upload.seek(0)

        self.assertEqual(doc.file.read(), self.upload.read())
        self.assertEqual(ParentBlob.objects.count(), 1)

        doc.file.seek(0)
        self.upload.seek(0)

        self.assertEqual(ParentBlob.objects.all()[0].file.read(),
                                                        self.upload.read())

    def test_auto_derived_blob_creation(self):
        """
        Test that a blob is created when using the file attribue on a derived
        document.
        """
        doc = Document(title='New Doc', file_name='A File', file=self.upload,
                                                                author=self.u1)
        doc.save()
        derived = DerivedDocument(derived_from=doc._blob, index=0,
                                                        file=self.upload2)
        derived.save()

        self.upload2.seek(0)
        self.upload.seek(0)

        self.assertEqual(derived.file.read(), self.upload2.read())
        self.assertEqual(DerivedBlob.objects.count(), 1)

        self.upload2.seek(0)
        derived.file.seek(0)

        self.assertEqual(DerivedBlob.objects.all()[0].file.read(),
                                                        self.upload2.read())

    def tearDown(self):
        self.u1.delete()
        Document.objects.all().delete()