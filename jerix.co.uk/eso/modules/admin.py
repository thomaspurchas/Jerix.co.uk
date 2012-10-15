from django.contrib import admin
from modules.models import Subject, AcademicYear, Module, ParentPost, SubPost, Material, History

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
    inlines = [
        MaterialInline,
    ]

class ParentPostAdmin(admin.ModelAdmin):
    """docstring for ParentPostAdmin"""

    search_fields = ('title',)
    list_display = ('__unicode__', 'module',)

    inlines = [
        SubPostInline,
        MaterialInline,
    ]

    class Media:
        js = ['js/collapsed_stacked_inlines.js']

class ModuleAdmin(admin.ModelAdmin):
    pass
    # filter_horizontal = ('lecturers',)

admin.site.register(Module, ModuleAdmin)
admin.site.register(ParentPost, ParentPostAdmin)
admin.site.register(SubPost, SubPostAdmin)
admin.site.register(Material)
admin.site.register(AcademicYear)
admin.site.register(Subject)
admin.site.register(History)