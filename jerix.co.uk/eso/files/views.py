# Create your views here.
import logging
from os import path

from django.shortcuts import redirect, get_object_or_404, render
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache

from files.models import Document, DerivedDocument

log = logging.getLogger(__name__)

URL_EXPIRY = getattr(settings, 'S3_URL_EXPIRES_IN', 30)

# s3conn = S3Connection(settings.AWS_ACCESS_KEY_ID,
#                    settings.AWS_SECRET_ACCESS_KEY,
#                    calling_format=VHostCallingFormat(),
#                    debug=2
#                    )
# s3bucket = s3conn.get_bucket('media.jerix.co.uk')


def generate_headers(filename, doc):
    if doc.type in ["pdf", "png"]:
        serve = "inline"
    else:
        serve = "attachment"

    headers = {
        'response-content-disposition': '%s; filename="%s"' % (serve, filename),
    }

    return headers


def generate_url(doc, headers):
    url = doc._blob.file.file.key.generate_url(
        URL_EXPIRY,
        force_http=True,
        response_headers=headers
    )
    return url


@login_required
@never_cache
def original_download(request, id, slug=None):
    doc = get_object_or_404(Document, pk=id)

    if path.splitext(doc.file_name)[1] == path.splitext(doc.file.name)[1]:
        filename = doc.file_name
    else:
        filename = doc.file_name + path.splitext(doc.file.name)[1]

    headers = generate_headers(filename, doc)

    url = generate_url(doc, headers)

    if doc.type in ["pdf"]:
        return render(request,
                      'files/pdf.html',
                      {
                          'S3_URL': url,
                      })
    else:
        return redirect(url)


@login_required
@never_cache
def derived_download(request, id, slug, orig_id=None):
    doc = get_object_or_404(DerivedDocument, pk=id)
    filename = path.basename(doc.file.name)
    if orig_id:
        orig_doc = get_object_or_404(Document, pk=orig_id)
        ext = path.splitext(filename)[1]
        filename = path.splitext(orig_doc.file_name)[0]
        filename += ext
    log.debug(orig_id)
    headers = generate_headers(filename, doc)

    url = generate_url(doc, headers)

    if doc.type in ["pdf"]:
        return render(request,
                      'files/pdf.html',
                      {
                          'S3_URL': url,
                      })
    else:
        return redirect(url)
