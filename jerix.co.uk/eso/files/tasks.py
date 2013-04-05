import logging
import os
import tempfile
import subprocess
import socket
import threading
import shutil
import re

from django.core.files.uploadedfile import UploadedFile, TemporaryUploadedFile

import Image
from celery import task

from files.models import ParentBlob, DerivedDocument, Document
from files.helpers import type_to_priorty

log = logging.getLogger(__name__)

UNOCONV_CALL = 'unoconv --timeout=10 --port=%s --output="%s" "%s"'
TIMEOUT = 60


def get_free_port():
    # Note this is super fuzzy, there are funky race conditions here, but they
    # shouldn't cause a problem most of the time
    s = socket.socket()
    s.bind(('', 0))
    port = s.getsockname()[1]
    s.close()
    return port


def timeout(p, port):
    log.info('Timeout for unoconv process with port %s fired. Retcode: %s' % (port, p.poll()))
    if p.poll() is None:
        log.error('unoconv process with port %s taking too long to complete--terminating' % port)
        p.terminate()

class ConversionError(Exception):
    def __init__(self, msg):
        self.msg = msg

@task(acks_late=True, queue='conversion', ignore_result=True)
def create_pdf(blob_pk):
    log.info('PDF Conversion start')
    blob = ParentBlob.objects.get(pk=blob_pk)
    orig_file = blob.file

    log.info('Starting conversion of %s to PDF' % blob)

    # Check for derived files of PDF type
    if blob.documents.filter(file_type='pdf'):
        log.info('%s is a PDF, no need to convert' % blob)
        return False
    elif blob.derived_documents.filter(file_type='pdf'):
        log.info('%s has derived PDF, no need to convert' % blob)
        return False

    tempd_loc = tempfile.mkdtemp()
    temp_file, tempf_loc = tempfile.mkstemp(dir=tempd_loc)

    temp_file = os.fdopen(temp_file, "wb")

    for chunk in orig_file.chunks():
        temp_file.write(chunk)
    temp_file.close()

    try:
        port = get_free_port()

        log.info("Launching unoconv with port %s" % port)

        proc = subprocess.Popen(UNOCONV_CALL % (port, tempd_loc, tempf_loc),
                                #stderr=subprocess.PIPE,
                                #stdout=subprocess.PIPE,
                                shell=True)

        # Create and start a watchdog thread
        t = threading.Timer(TIMEOUT, timeout, [proc, port])
        t.start()

        stderr, stdout = None, None#proc.communicate()
        proc.wait()

        t.cancel()

        if proc.returncode != 0:
            error = subprocess.CalledProcessError(proc.returncode,
                                                  UNOCONV_CALL % (
                                                  port, tempd_loc, tempf_loc))
            error.output = "%s %s" % (stderr, stdout)
            raise error

        log.info("unoconv (port %s) output: %s %s" % (port, stderr, stdout))

    except subprocess.CalledProcessError as e:
        log.error('unoconv (port %s) returned a non-zero exit status: %s' % (port, e.output))

    os.unlink(tempf_loc)

    files = os.listdir(tempd_loc)

    for pdf in files:
        if pdf.lower().endswith('.pdf'):
            break
    else:
        shutil.rmtree(tempd_loc, True)
        raise ConversionError('Unable to find PDF file')

    pdf = os.path.abspath(os.path.join(tempd_loc, pdf))
    pdf = open(pdf, 'rb')
    filename = os.path.basename(orig_file.name)
    filename = os.path.splitext(filename)[0] + '.pdf'

    doc = DerivedDocument(derived_from=blob)
    doc.file = UploadedFile(pdf, filename, 'application/pdf', 0, None)
    doc.index = type_to_priorty('pdf')

    # # Do one last check before saving the blob, just incase this task got fired
    # # twice in quick succession.

    if blob.derived_documents.filter(_blob__file_type='pdf'):
        return False
    else:
        doc.save()

    pdf.close()

    shutil.rmtree(tempd_loc, True)

    log.info("Convertion of %s complete" % blob)

    return True


@task(acks_late=True, queue='conversion', ignore_result=True)
def create_pngs(document_pk, type='pngs'):
    doc = Document.objects.get(pk=document_pk)
    blob = doc._blob
    log.info('Starting png generation of: %s', doc)

    # Check to make sure that we don't already have a pngs pack
    # Check for derived files of PDF type
    if doc.file_type == 'png':
        log.info('%s is a PNG, no need to convert' % blob)
        return False
    elif blob.derived_documents.filter(file_type='png'):
        log.info('%s has derived PNG, no need to convert' % blob)
        return False

    # Locate a pdf file
    if doc.type == 'pdf':
        pdf = doc
    else:
        pdf = doc.get_derived_documents_of_type('pdf')
        if pdf:
            pdf = pdf[0]

    if not pdf:
        log.info("No PDF avaliable for %s" % blob)

    # Create a temp folder
    temp_folder = tempfile.mkdtemp()
    log.debug('working with: %s', temp_folder)

    file = tempfile.NamedTemporaryFile(dir=temp_folder, delete=False)

    for data in pdf.file.chunks():
        file.write(data)
    file.close()

    # Now call ghostscript
    return_code = subprocess.call(["gs", "-sDEVICE=png16m",
        "-sOutputFile=%s/slide-%s.png" % (temp_folder, '%03d'),
        "-r600", "-dNOPAUSE", "-dBATCH", "-dMaxBitmap=1000000000",
        #"-dFirstPage=1", "-dLastPage=1",
        "%s" % file.name])

    if return_code != 0:
        log.error('Ghostscript error')
        # Clean up
        shutil.rmtree(temp_folder)
        create_pngs.retry()

    # Process the generated files with PIL

    # First generate a list of file in the tempdir
    compiled_regex = re.compile('^slide-(\w+).png$')
    scaled_images = {}
    for file in os.listdir(temp_folder):
        # Check using regex
        match = re.match(compiled_regex, file)
        if match:
            log.debug('scaling image: %s', file)
            order = int(match.group(1))

            # Resize using PIL
            slide = Image.open(os.path.join(temp_folder, file))
            slide.thumbnail((1920, 1200), Image.ANTIALIAS)

            new_filename = os.path.join(temp_folder, 'slide-scaled-%03d.png' % order)
            slide.save(new_filename)
            scaled_images[order] = new_filename

    # Make sure that the order starts at 0 and has no gaps
    new_images = {}
    order = 0
    sorted_keys = scaled_images.keys()
    sorted_keys.sort()
    for item in [scaled_images[key] for key in sorted_keys]:
        new_images[order] = item
        order += 1
    scaled_images = new_images


    # Before uploading check that there are still no other pngs up there.
    if blob.derived_documents.filter(file_type='png'):
        log.info('%s has derived PNG now, canceling upload' % blob)
        return False

    # Now go through all the generated slides and upload
    # Create a new derivedfile pack
    try:
        for order, filename in scaled_images.iteritems():
            file = open(filename, 'rb')

            parts = os.path.split(filename)
            filename = os.path.join(parts[-2], '%s_%s' % (
                doc.file_name[0:60], parts[-1]))

            upfile = TemporaryUploadedFile(filename, 'image/png', 0, None)
            upfile.file = file

            derived_doc = DerivedDocument(derived_from=blob)
            derived_doc.file = upfile
            derived_doc.index = order

            derived_doc.save()
    except:
        log.error(filename)
        raise

    shutil.rmtree(temp_folder)

    return True
