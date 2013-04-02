from django.contrib.auth.models import User
from django.db import models
from tastypie.models import create_api_key

models.signals.post_save.connect(create_api_key, sender=User)

from django.conf.urls import *
from modules.api import ModuleResource, SubjectResource, YearResource, TagResource

module_resource = ModuleResource()
subject_resource = SubjectResource()
year_resource = YearResource()
tag_resource = TagResource()

urlpatterns = patterns('',
    (r'^1.0/', include(module_resource.urls)),
    (r'^1.0/', include(subject_resource.urls)),
    (r'^1.0/', include(year_resource.urls)),
    (r'^1.0/', include(tag_resource.urls)),
)
