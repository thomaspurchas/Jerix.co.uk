import logging

from django.http import Http404, HttpResponse
from django.template import RequestContext
from django.shortcuts import render, redirect, get_object_or_404
from django.core.cache import cache

from accounts.models import UserProfile
from q_and_a.models import Question
from modules.models import AcademicYear

log = logging.getLogger(__name__)

# Create your views here.

def home(request):
    user = request.user

    col_1 = cache.get('home_col_1_%s' % user.username)
    col_2 = cache.get('home_col_2_%s' % user.username)

    if col_1 == None or col_2 == None:
        # Create values and put them in cache
        modules = []
        items = []

        if request.user.is_authenticated():
            profile = user.get_profile()
            if profile.is_student():
                student_profile = profile.student_profile

                modules = student_profile.modules.all()
                lecturers = UserProfile.objects.filter(
                                lecturer_profile__modules__students=student_profile)

                items.append(('modules', modules))
                items.append(('lecturers', lecturers))

        else:
            years = AcademicYear.objects.select_related().all().order_by(
                                                                   'short_code')

            print years
            i = 0
            for year in years:
                i += 1
                items.append(('year_%d' % i, year))

        questions = Question.objects.all().order_by('-asked')[:10]

        items.insert(0, ('questions', questions))
        print items

        col_1 = []
        col_2 = []

        iterator = iter(items)

        while True:
            try:
                col_1.append(iterator.next())
                col_2.append(iterator.next())
            except StopIteration:
                break
        log.debug('Column 1 contains: %s' % col_1)
        log.debug('Column 2 contains: %s' % col_2)

        if user.is_authenticated():
            cache.set('home_col_1_%s' % user.username, col_1, 10)
            cache.set('home_col_1_%s' % user.username, col_2, 10)
        else:
            cache.set('home_col_1_%s' % user.username, col_1, 30)
            cache.set('home_col_1_%s' % user.username, col_2, 30)


    context = {
        'col_1': col_1,
        'col_2': col_2
    }

    return render(request,
        'core/home.html',
        context
    )
