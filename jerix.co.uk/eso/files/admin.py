from os.path import basename

from django.contrib import admin
from django import forms

from django.core.files.uploadedfile import UploadedFile

from files.models import Document, DerivedDocument, ParentBlob, DerivedBlob

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        #exclude = ('_blob')

    file = forms.FileField(required=True)

    def __init__(self, *args, **kwargs):
        new = False if kwargs.get('instance') else True
        if not kwargs.get('initial') and not new:
            kwargs['initial'] = {'file': kwargs['instance']._blob.file}
        super(DocumentForm, self).__init__(*args, **kwargs)
        self.fields['title'].required = False
        self.fields['file_name'].required = False

class DerivedDocumentForm(forms.ModelForm):
    class Meta:
        model = DerivedDocument

    file = forms.FileField(required=True)

    def __init__(self, *args, **kwargs):
        new = False if kwargs.get('instance') else True
        if not kwargs.get('initial') and not new:
            kwargs['initial'] = {'file': kwargs['instance']._blob.file}
        super(DerivedDocumentForm, self).__init__(*args, **kwargs)

class ParentBlobAdmin(admin.ModelAdmin):
    readonly_fields = ('md5_sum', 'file', 'extraction_error')

class DerivedBlobAdmin(admin.ModelAdmin):
    readonly_fields = ('md5_sum', 'upload_to_url', 'file', 'extraction_error')

class DocumentAdmin(admin.ModelAdmin):
    form = DocumentForm
    exclude = ['_blob']
    readonly_fields = ('extraction_error', 'file_type')

    list_filter = ('file_type', )
    list_display = ('__unicode__', 'file_type')
    search_fields = ('file_name', 'title')

    # def add_view(self, *args, **kargs):
    #     self.exclude.append('file_name')
    #     return super(DocumentAdmin, self).add_view(*args, **kargs)

    def save_model(self, request, obj, form, change):
        if isinstance(form.cleaned_data['file'], UploadedFile):
            obj.file = form.cleaned_data['file']
        obj.save()
        if obj.file_name.strip() == '':
            obj.file_name = basename(obj.file.name)

        if obj.title.strip() == '':
            obj.title = obj.file_name
        obj.save()

class DerivedDocumentAdmin(admin.ModelAdmin):
    form = DerivedDocumentForm
    exclude = ['_blob']
    readonly_fields = ('extraction_error', 'file_type')

    list_filter = ('file_type', )
    list_display = ('__unicode__', 'file_type')

    def save_model(self, request, obj, form, change):
        if isinstance(form.cleaned_data['file'], UploadedFile):
            obj.file = form.cleaned_data['file']
        obj.save()

admin.site.register(ParentBlob, ParentBlobAdmin)
admin.site.register(DerivedBlob, DerivedBlobAdmin)
admin.site.register(Document, DocumentAdmin)
admin.site.register(DerivedDocument, DerivedDocumentAdmin)
