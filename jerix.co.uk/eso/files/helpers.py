import os
import re
import hashlib

from django.conf import settings
from django.core.files import File
from django.core.exceptions import ImproperlyConfigured

from files.errors import CannotIdentifyFileTypeError, ReadOnlyFileError

compiled_regexs = {}
type_to_path = {}
type_to_display_cache = {}
type_to_priorty_cache = {}


def _compile_regexs():
    """"""
    for regex, info in settings.FILE_TYPE_MAPPINGS.items():
        compiled = re.compile(regex)
        file_type = info['type']
        compiled_regexs[compiled] = file_type


def _generate_type_to_path():
    """"""
    for _, info in settings.FILE_TYPE_MAPPINGS.items():
        type_to_path[info['type']] = info['path']


def _generate_type_to_display_cache():
    for _, info in settings.FILE_TYPE_MAPPINGS.items():
        type_to_display_cache[info['type']] = unicode(
                                            info.get('display', info['type']))


def _generate_type_to_priorty_cache():
    for _, info in settings.FILE_TYPE_MAPPINGS.items():
        type_to_priorty_cache[info['type']] = int(info.get('priority', 0))

# Helper funtions


def type_to_display(type):
    return type_to_display_cache.get(type, type)


def type_to_priorty(type):
    return type_to_priorty_cache.get(type, 0)


def identify_file_type(name):
    """docstring for get_file_type"""
    name = os.path.basename(name)
    for regex, file_type in compiled_regexs.items():
        if regex.match(name):
            return file_type
    else:
        return None


def generate_md5(file):
    m = hashlib.md5()
    file.seek(0)
    for chunk in file.chunks():
        m.update(chunk)
    return m.hexdigest()


def identify_and_md5(file):
    """docstring for identify_and_mdf"""
    file_type = identify_file_type(file.name)
    if not file_type:
        raise CannotIdentifyFileTypeError(file)
    md5_sum = generate_md5(file)
    file.seek(0)
    return (file_type, md5_sum)


def get_path(file_type):
    path = type_to_path[file_type]
    if path == None:
        raise ImproperlyConfigured(
                'Type "%s" does not have a derived path' % file_type)
    return path


class ReadOnlyFile(File):
    def write(self, *args, **kargs):
        raise ReadOnlyFileError('Cannot write to file')

    def delete(self, *args, **kargs):
        raise ReadOnlyFileError('Cannot delete file')

    save = write
    write = write
    writelines = write
    delete = delete

_compile_regexs()
_generate_type_to_path()
_generate_type_to_display_cache()
_generate_type_to_priorty_cache()
