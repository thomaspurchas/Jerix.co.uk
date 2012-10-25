from django.http import Http404, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect, get_object_or_404

from accounts.models import UserProfile
from q_and_a.models import Question

# Create your views here.

def home(request):
    user = request.user
    modules = []
    items = {}
    if request.user.is_authenticated():
        profile = user.get_profile()
        if profile.is_student():
            student_profile = profile.student_profile

            modules = student_profile.modules.all()
            lecturers = UserProfile.objects.filter(
                            lecturer_profile__modules__students=student_profile)

            items.update({
                'modules': modules,
                'lecturers': lecturers
            })

    questions = Question.objects.all().order_by('-asked')[:10]

    items.update({
        'questions': questions,
    })

    col_1 = []
    col_2 = []

    iterator = items.iteritems()

    while True:
        try:
            col_1.append(iterator.next())
            col_2.append(iterator.next())
        except StopIteration:
            break
    print col_1
    print col_2
    context = {
        'col_1': col_1,
        'col_2': col_2
    }

    return render_to_response(
        'core/home.html',
        context,
        RequestContext(request)
    )
