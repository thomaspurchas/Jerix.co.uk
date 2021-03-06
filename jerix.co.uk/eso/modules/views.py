import logging
import datetime

from django.http import Http404
from django.shortcuts import render, redirect
from django.db.models import Q
from django.template.defaultfilters import slugify
from django.core.cache import cache

from modules.models import Module, ParentPost
from q_and_a.models import Question

logger = logging.getLogger(__name__)

# Create your views here.


def module_posts(request, module_id, slug=None):
    try:
        module = cache.get('module_posts_%s_module' % module_id)
        if not module:
            module = Module.objects.get(pk=module_id)
            cache.set('module_posts_%s_module' % module_id, module, 60 * 10)

        if slug != slugify(module.title):
            return redirect('module-posts',
                            module_id=module_id, slug=slugify(module.title),
                            permanent=False)
        posts = cache.get('module_posts_%s_posts' % module_id)
        if not posts:
            posts = ParentPost.objects.filter(module=module)
            posts = posts.filter(
                Q(historical_period__start_date__lte=datetime.date.today()) |
                Q(historical_period=None)
            )
            posts = posts.exclude(
                historical_period__end_date__lte=datetime.date.today())

            cache.set('module_posts_%s_posts' % module_id, posts, 60 * 0.5)

        # Prefetch materials, and documents
        rel = 'materials__document___blob__derived_documents___blob'
        posts = posts.prefetch_related(rel)

        # Get related questions by looking up the modules `primary_tag`
        questions = cache.get('modules_posts_%s_questions' % module_id)
        if not questions:
            questions = Question.objects.filter(tags=module.primary_tag)
            questions = questions.distinct().order_by('asked')[:10]
            cache.set('module_posts_%s_questions' % module_id, questions, 60 * 1)

    except Module.DoesNotExist:
        raise Http404
    return render(request,
                  'modules/posts.html',
                  {
                      'module': module,
                      'posts': posts,
                      'questions': questions,
                  }
                  )
