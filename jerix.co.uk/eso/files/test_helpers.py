import os

from files.models import Document, DerivedDocument, ParentBlob, DerivedBlob

from files.helpers import identify_file_type, identify_and_md5, get_path

# Test helpers
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
        blob.save()
    document = Document()
    document.file_name = os.path.basename(file.name)
    document._blob = blob

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
        blob.upload_to_url = get_path(file_type)
        blob.save()

    document = DerivedDocument()
    document._blob = blob

    return document
