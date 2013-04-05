from django.db.models.signals import pre_delete

from sorl.thumbnail import delete
from files.models import ParentBlob, DerivedBlob

def cleanup_thumbnail(sender, instance, **kargs):
    """
    Cleans up thumbnails when blob is deleted
    """
    if instance.file.name.endswith('.png'):
        delete(instance.file)

pre_delete.connect(cleanup_thumbnail, ParentBlob)
pre_delete.connect(cleanup_thumbnail, DerivedBlob)
