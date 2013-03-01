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
