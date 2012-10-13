from django.http import Http404, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect, get_object_or_404

from accounts.models import LecturerProfile

# Create your views here.

def home(request):
    user = request.user
    modules = []
    if request.user.is_authenticated():
        profile = user.get_profile()
        if profile.is_student():
            student_profile = profile.student_profile

            modules = student_profile.modules.all()
            lecturers = LecturerProfile.objects.filter(
                                            modules__students=student_profile)
            lecturers = LecturerProfile.objects.all()
            print lecturers

    return render_to_response(
        'core/home.html',
        {
            'modules': modules,
            'lecturers': lecturers
        },
        RequestContext(request)
    )
