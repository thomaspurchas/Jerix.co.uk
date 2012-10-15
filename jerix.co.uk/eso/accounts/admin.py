from django.contrib import admin
from accounts.models import UserProfile, LecturerProfile, StudentProfile

class UserProfileInline(admin.StackedInline):
    model = UserProfile

class LecturerProfileAdmin(admin.ModelAdmin):
    filter_horizontal = ('modules',)
    inlines = [
        UserProfileInline,
    ]

class StudentProfileAdmin(admin.ModelAdmin):
    filter_horizontal = ('modules',)
    inlines = [
        UserProfileInline,
    ]

admin.site.register(UserProfile)
admin.site.register(LecturerProfile, LecturerProfileAdmin)
admin.site.register(StudentProfile, StudentProfileAdmin)
