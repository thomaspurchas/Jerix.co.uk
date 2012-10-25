from django.db.models.signals import post_save
from django.dispatch import receiver

from files.models import Document

@receiver(post_save, sender=Document)
def convert_to_pdf(sender, instance, created, raw, **kargs):
    from files.tasks import create_pdf
    if created and not raw:
        print 'Firing create_pdf task with %s:%s' % (instance, instance.pk)
        create_pdf.delay(instance.pk)
    else:
        print 'Not firing create_pdf task with %s:%s' % (instance, instance.pk)