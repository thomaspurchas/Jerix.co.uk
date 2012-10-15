import logging
import datetime

from django.http import Http404
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from django.db.models import Q
from django.template.defaultfilters import slugify
from django.views.decorators.cache import cache_page

from modules.models import Module
from q_and_a.models import Question

# Create your views here.
@cache_page(60 * 2)
def module_posts(request, module_id, slug=None):
    try:
        module = Module.objects.get(pk=module_id)
        if slug != slugify(module.title):
            print 'redirect'
            return redirect('module-posts',
                module_id=module_id, slug=slugify(module.title),
                permanent=False)
        posts = module.posts.filter(
            Q(historical_period__start_date__lte=datetime.date.today()) |
            Q(historical_period=None)
        )
        posts = posts.exclude(
                        historical_period__end_date__lte=datetime.date.today())

        # Prefetch materials, and documents
        posts = posts.prefetch_related('materials__document')

        # Get related questions by looking up the modules `primary_tag`
        questions = Question.objects.filter(tags=module.primary_tag).distinct()
        questions = questions.order_by('asked')[:10]
    except Module.DoesNotExist:
        raise Http404
    return render_to_response(
        'modules/module_posts.html',
        {
            'module': module,
            'posts': posts,
            'questions': questions,
        },
        RequestContext(request)
    )