import logging
import mimetypes
import urllib2
import os

from django.core.files.uploadedfile import TemporaryUploadedFile

from celery.task import task
from poster.streaminghttp import register_openers

from files.models import Document, DerivedDocument
from files.helpers import type_to_priorty

log = logging.getLogger(__name__)

# Register the streaming http handlers with urllib2
register_openers()

JOD_URL = 'http://localhost:8080/converter/service'

@task(acks_late=True)
def create_pdf(document_pk):
    log.info('PDF Conversion start')
    doc = Document.objects.get(pk=document_pk)
    file = doc.file

    log.info('Starting conversion of %s to PDF' % doc)

    # Check for derived files of PDF type
    if doc.type == 'pdf':
        return False
    elif doc.get_derived_documents_of_type('pdf'):
        return False

    file.seek(0)

    # Botched file streaming
    headers = {}

    filesize = file.size

    headers['Content-Type'] = mimetypes.guess_type(file.name)[0]
    headers['Accept']= "application/pdf"
    headers['Content-Length'] = '%s' % filesize

    def yielder():
        while True:
            block = file.read(10240)
            if block:
                yield block
            else:
                break

    try:
        req = urllib2.Request(JOD_URL, yielder(), headers)

        # Get the return file
        return_file = urllib2.urlopen(req)

        filename = os.path.basename(file.name)
        filename = os.path.splitext(filename)[0] + '.pdf'

        new_file = TemporaryUploadedFile(filename, 'application/pdf', 0, None)
        while True:
            data = return_file.read(10240)
            if data:
                new_file.write(data)
            else:
                new_file.size = os.path.getsize(new_file.temporary_file_path())
                break

    except urllib2.HTTPError as e:
        msg = e.msg
        if e.fp:
            msg += ' - %s' % e.fp.read()
        log.error('Conversion service error: %s - %s - %s', e.hdrs, e.code, msg)
        create_pdf.retry(exc=e)

    derived_doc = DerivedDocument()
    derived_doc.derived_from = doc._blob
    derived_doc.file = new_file
    derived_doc.index = type_to_priorty('pdf')

    derived_doc.save()

    return True