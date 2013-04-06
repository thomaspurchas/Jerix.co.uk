import logging

from django.db.models.signals import post_save
from django.dispatch import receiver

from files.models import ParentBlob, DerivedBlob, Document, DerivedDocument
from files.tasks import create_pdf, create_pngs, create_thumbs

log = logging.getLogger(__name__)


@receiver(post_save, sender=ParentBlob)
def convert_to_pdf(sender, instance, created, raw, **kargs):
    if created and not raw:
        doc = instance.documents.all()[0]
        log.info('Firing create_pdf task with %s:%s' % (doc, doc.pk))
        create_pdf.delay(doc.pk)


def convert_to_pngs(sender, instance, created, raw, **kargs):
    if created and not raw:
        if sender == Document:
            log.info("Getting doc for Document %s" % instance)
            doc = instance
        elif sender == DerivedDocument:
            log.info("Getting doc for DerivedDocument %s" % instance)
            doc = instance.derived_from.documents.all()[0]

        if doc.file_type == 'png':
            return
        elif doc.get_derived_documents_of_type(file_type='png'):
            return
        log.info('Firing create_pngs task with %s:%s' % (doc, doc.pk))
        create_pngs.delay(doc.pk)

post_save.connect(convert_to_pngs, Document)
post_save.connect(convert_to_pngs, DerivedDocument)


def create_thumbnails(sender, instance, created, raw, **kwargs):
    if created and not raw:
        doc = instance
        log.info('Firing create_thumbs task with %s:%s' % (doc, doc.pk))
        create_thumbs.delay(doc.pk)

post_save.connect(create_thumbnails, DerivedDocument)
