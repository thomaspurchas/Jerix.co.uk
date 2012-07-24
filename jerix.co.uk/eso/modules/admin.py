from django.contrib import admin
from modules.models import Module, ParentPost, SubPost, Material

class MaterialInline(admin.TabularInline):
    """docstring for MaterialInline"""
    model = Material
    extra = 3

class SubPostInline(admin.TabularInline):
    """docstring for SubPostInline"""
    model = SubPost
    fk_name = 'parent'
    extra = 2
    classes = ['collapse', 'collapsed']

class SubPostAdmin(admin.ModelAdmin):
    """docstring for SubPostAmdin"""
    inlines = [MaterialInline]

class ParentPostAdmin(admin.ModelAdmin):
    """docstring for ParentPostAdmin"""

    search_fields = ('title',)
    list_display = ('__unicode__', 'module',)

    inlines = [SubPostInline, MaterialInline]

    class Media:
        js = ['js/collapsed_stacked_inlines.js']

admin.site.register(Module)
admin.site.register(ParentPost, ParentPostAdmin)
admin.site.register(SubPost, SubPostAdmin)
admin.site.register(Material)