import os
import re
import hashlib

from django.conf import settings

from files.errors import CannotIdentifyFileType
from files.models import Document, DerivedDocument, ParentBlob, DerivedBlob

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

def uploaded_new_document(file):
    """
    Sets up a new document object ready to be saved.
    Note that it won't fill in the `title` or `author` attributes,
    you have to do that.
    """
    file_type, md5_sum = identify_and_md5(file)
    try:
        blob = ParentBlob.objects.get(md5_sum=md5_sum)
    except ParentBlob.DoesNotExist:
        blob = ParentBlob.objects.create(md5_sum=md5_sum, file=file,
                                            file_type=file_type)
    document = Document()
    document.file_name = os.path.basename(file.name)
    document.blob = blob
    
    return document
    
def uploaded_new_derived_document(file):
    """
    Like `uploaded_new_derived_document' this creates the 'DerivedBlob' 
    object and a 'DerivedDocument' object.
    
    The `DerivedDocument` object is returned, you need to fill in 
    `derived_from` and `index`.
    """
    file_type, md5_sum = identify_and_md5(file)
    try:
        blob = DerivedBlob.objects.get(md5_sum=md5_sum)
    except DerivedBlob.DoesNotExist:
        blob = DerivedBlob(md5_sum=md5_sum, file=file, file_type=file_type)
        blob.upload_to_url = type_to_path[file_type]
        blob.save()
        
    document = DerivedDocument()
    document.blob = blob
    
    return document
    
_compile_regexs()
_generate_type_to_path()