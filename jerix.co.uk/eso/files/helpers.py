import os
import re
import hashlib

from django.conf import settings

from files.errors import CannotIdentifyFileType

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

def identify_and_md5(file):
    """docstring for identify_and_mdf"""
    file_type = identify_file_type(file.name)
    if not file_type:
        raise CannotIdentifyFileType(file)
    m = hashlib.md5()
    for chunk in file.chunks():
        m.update(chunk)
    md5_sum = m.hexdigest()
    return (file_type, md5_sum)
    
def get_path(file_type):
    return type_to_path[file_type]
    
_compile_regexs()
_generate_type_to_path()