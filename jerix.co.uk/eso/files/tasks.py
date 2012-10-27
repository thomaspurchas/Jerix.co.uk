import logging
import mimetypes
import urllib2
import os

from django.core.files.uploadedfile import TemporaryUploadedFile

from celery.task import task
from poster.streaminghttp import register_openers

from files.models import ParentBlob, DerivedDocument
from files.helpers import type_to_priorty

log = logging.getLogger(__name__)

# Register the streaming http handlers with urllib2
register_openers()

JOD_URL = 'http://localhost:8080/converter/service'

@task(acks_late=True)
def create_pdf(blob_pk):
    log.info('PDF Conversion start')
    blob = ParentBlob.objects.get(pk=blob_pk)
    file = blob.file

    log.info('Starting conversion of %s to PDF' % blob)

    # Check for derived files of PDF type
    if blob.file_type == 'pdf':
        return False
    elif blob.derived_documents.filter(_blob__file_type='pdf'):
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
    derived_doc.derived_from = blob
    derived_doc.file = new_file
    derived_doc.index = type_to_priorty('pdf')

    # Do one last check before saving the blob, just incase this task got fired
    # twice in quick succession.

    if blob.derived_documents.filter(_blob__file_type='pdf'):
            return False
    else:
        derived_doc.save()

    return True