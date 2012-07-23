from django.contrib import admin
from modules.models import Module, ParentPost, SubPost, Material

admin.site.register(Module)
admin.site.register(ParentPost)
admin.site.register(SubPost)
admin.site.register(Material)