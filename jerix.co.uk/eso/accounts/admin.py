from django.contrib import admin
from accounts.models import UserProfile, LecturerProfile, StudentProfile

class LecturerProfileAdmin(admin.ModelAdmin):
    pass

admin.site.register(UserProfile)
admin.site.register(LecturerProfile, LecturerProfileAdmin)
admin.site.register(StudentProfile)
