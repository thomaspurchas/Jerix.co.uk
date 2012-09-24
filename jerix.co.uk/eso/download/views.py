# Create your views here.
from os import path

from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.conf import settings

from boto.s3.connection import S3Connection, VHostCallingFormat

from files.models import Document, DerivedDocument

# s3conn = S3Connection(settings.AWS_ACCESS_KEY_ID,
#                    settings.AWS_SECRET_ACCESS_KEY,
#                    calling_format=VHostCallingFormat(),
#                    debug=2
#                    )
# s3bucket = s3conn.get_bucket('media.jerix.co.uk')

def generate_headers(filename, doc):
    if doc.type == "pdf":
        serve = "inline"
    else:
        serve = "attachment"

    headers = {
        'response-content-disposition': '%s; filename="%s"' % (serve, filename),
    }

    return headers

def generate_url(doc, headers):
    url = doc._blob.file.file.key.generate_url(
                                                30,
                                                force_http=True,
                                                response_headers=headers
                                               )
    return url

def original_download(request, id, slug=None):
    doc = get_object_or_404(Document, pk=id)

    if path.splitext(doc.file_name)[1] == path.splitext(doc.file.name)[1]:
        filename = doc.file_name
    else:
        filename = doc.file_name + path.splitext(doc.file.name)[1]

    headers = generate_headers(filename, doc)

    url = generate_url(doc, headers)

    return redirect(url)

def derived_download(request, id, slug, orig_id=None):
    doc = get_object_or_404(DerivedDocument, pk=id)
    filename = path.basename(doc.file.name)
    if orig_id:
        orig_doc = get_object_or_404(Document, pk=orig_id)
        ext = path.splitext(filename)[1]
        filename = path.splitext(orig_doc.file_name)[0]
        filename += ext
    print orig_id
    headers = generate_headers(filename, doc)

    url = generate_url(doc, headers)

    return redirect(url)