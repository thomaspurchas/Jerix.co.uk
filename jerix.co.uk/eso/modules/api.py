from tastypie.authentication import ApiKeyAuthentication
from tastypie.authorization import DjangoAuthorization

from tastypie.resources import ModelResource, ALL
from tastypie import fields
from modules.models import Module, Subject, AcademicYear
from taggit.models import Tag

class SubjectResource(ModelResource):
    
    class Meta:
        queryset = Subject.objects.all()
        resource_name = 'subject'
        authentication = ApiKeyAuthentication()
        authorization = DjangoAuthorization()

class ModuleResource(ModelResource):
    
    subject = fields.ToOneField('modules.api.SubjectResource', 'subject')
    year = fields.ToOneField('modules.api.YearResource', 'year')
    primary_tag = fields.ToOneField('modules.api.TagResource', 'primary_tag')
    
    class Meta:
        queryset = Module.objects.all()
        resource_name = 'module'
        authentication = ApiKeyAuthentication()
        authorization = DjangoAuthorization()
        filtering = {
                    'short_code': ALL,
                    'title': ALL,
                }
        
class YearResource(ModelResource):
    
    class Meta:
        queryset = AcademicYear.objects.all()
        resource_name = 'year'
        authentication = ApiKeyAuthentication()
        authorization = DjangoAuthorization()
        filtering = {
                    'title': ALL,
                }
        
class TagResource(ModelResource):
    
    class Meta:
        queryset = Tag.objects.all()
        resource_name = 'tag'
        authentication = ApiKeyAuthentication()
        authorization = DjangoAuthorization()
        filtering = {
                    'name': ALL,
                    'slug': ALL,
                }