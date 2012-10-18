import celery
from celery.task import task

def with_document(fn):
    def wrapped(document_pk, *args, **kargs):
        doc = None
        return fn(doc, *args, **kargs)

    return wrapped

@task(acks_late=True)
@with_document
def create_pdf(document, type='pdf', callback=None):
    pass