from django.utils.functional import LazyObject
from django.core.files.storage import get_storage_class
from django.conf import settings

class StaticStorage(LazyObject):
    def _setup(self):
        self._wrapped = get_storage_class(
        'storages.backends.s3boto.S3BotoStorage')(bucket='static.jerix.co.uk')
