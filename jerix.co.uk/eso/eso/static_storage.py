from django.core.files.storage import get_storage_class
from storages.backends.s3boto import S3BotoStorage

class StaticStorage(S3BotoStorage):
    """
    S3 storage backend that saves the files locally, too.
    """
    def __init__(self, *args, **kwargs):
        kwargs['bucket'] = 'static.jerix.co.uk'
        kwargs['custom_domain'] = 'static.jerix.co.uk'
        super(StaticStorage, self).__init__(*args, **kwargs)
        self.local_storage = get_storage_class(
            "compressor.storage.CompressorFileStorage")()

    def save(self, name, content):
        name = super(StaticStorage, self).save(name, content)
        self.local_storage._save(name, content)
        return name

    def url(self, name):
        """A quick hack to prevent boto from removing trailing slashes"""
        slash = name.replace('\\','/')[-1] == '/'
        url = super(StaticStorage, self).url(name)
        if slash:
            url += '/'
        return url