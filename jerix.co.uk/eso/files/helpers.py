import os
import re
import hashlib

from django.conf import settings
from django.core.files import File

from files.errors import CannotIdentifyFileTypeError, ReadOnlyFileError

compiled_regexs = {}
type_to_path = {}

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

# Helper funtions
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
    for chunk in file.chunks():
        m.update(chunk)
    return m.hexdigest()


def identify_and_md5(file):
    """docstring for identify_and_mdf"""
    file_type = identify_file_type(file.name)
    if not file_type:
        raise CannotIdentifyFileTypeError(file)
    md5_sum = generate_md5(file)
    return (file_type, md5_sum)

def get_path(file_type):
    return type_to_path[file_type]

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