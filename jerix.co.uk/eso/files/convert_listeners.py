from django.db.models.signals import post_save
from django.dispatch import receiver

from files.models import ParentBlob

@receiver(post_save, sender=ParentBlob)
def convert_to_pdf(sender, instance, created, raw, **kargs):
    from files.tasks import create_pdf
    print 'Covert to PDF'
    if not raw:
        print 'Firing create_pdf task with %s:%s' % (instance, instance.pk)
        create_pdf.delay(instance.pk)