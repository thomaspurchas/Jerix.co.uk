"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User

from files.models import Document
from files.helpers import uploaded_new_document, uploaded_new_derived_document

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
        derived.derived_from = doc.blob
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
        derived.derived_from = doc.blob
        derived.index = 0
        derived.save()

    def tearDown(self):
        self.u1.delete()
        Document.objects.all().delete()