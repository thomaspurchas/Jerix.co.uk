import logging

from django.db.models.signals import post_save
from django.dispatch import receiver

from files.models import ParentBlob

log = logging.getLogger(__name__)

@receiver(post_save, sender=ParentBlob)
def convert_to_pdf(sender, instance, created, raw, **kargs):
    from files.tasks import create_pdf
    if created and not raw:
        log.info('Firing create_pdf task with %s:%s' % (instance, instance.pk))
        create_pdf.delay(instance.pk)