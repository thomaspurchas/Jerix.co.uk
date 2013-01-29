from django.contrib import admin
from accounts.models import UserProfile, LecturerProfile, StudentProfile

class UserProfileInline(admin.StackedInline):
    model = UserProfile

class LecturerProfileAdmin(admin.ModelAdmin):
    filter_horizontal = ('modules',)
    exclude = ('user_profile',)

class StudentProfileAdmin(admin.ModelAdmin):
    filter_horizontal = ('modules',)
    exclude = ('user_profile',)

admin.site.register(UserProfile)
admin.site.register(LecturerProfile, LecturerProfileAdmin)
admin.site.register(StudentProfile, StudentProfileAdmin)

from tastypie.admin import ApiKeyInline
from tastypie.models import ApiAccess, ApiKey
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

admin.site.register(ApiKey)
admin.site.register(ApiAccess)

class UserModelAdmin(UserAdmin):
    inlines = UserAdmin.inlines + [ApiKeyInline]

admin.site.unregister(User)
admin.site.register(User,UserModelAdmin)
