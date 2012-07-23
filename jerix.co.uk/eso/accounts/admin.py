from django.contrib import admin
from accounts.models import UserProfile, LecturerProfile, StudentProfile

admin.site.register(UserProfile)
admin.site.register(LecturerProfile)
admin.site.register(StudentProfile)
