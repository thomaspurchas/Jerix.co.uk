from django.http import Http404, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect, get_object_or_404

from accounts.models import UserProfile

# Create your views here.

def home(request):
    user = request.user
    modules = []
    if request.user.is_authenticated():
        profile = user.get_profile()
        if profile.is_student():
            student_profile = profile.student_profile

            modules = student_profile.modules.all()
            lecturers = UserProfile.objects.filter(
                            lecturer_profile__modules__students=student_profile)

    return render_to_response(
        'core/home.html',
        {
            'modules': modules,
            'lecturers': lecturers
        },
        RequestContext(request)
    )
