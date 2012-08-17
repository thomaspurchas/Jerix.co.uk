import datetime

from django.http import Http404
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from django.db.models import Q
from django.template.defaultfilters import slugify

from modules.models import Module
# Create your views here.
def module_posts(request, module_id, slug=None):
    try:
        module = Module.objects.get(pk=module_id)
        print slugify(module.title)
        print slug
        if slug != slugify(module.title):
            print 'redirect'
            return redirect('module-posts',
                module_id=module_id, slug=slugify(module.title),
                permanent=False)
        posts = module.posts.filter(
            Q(historical_period__start_date__lt=datetime.date.today()) |
            Q(historical_period=None)
        )
        posts = posts.exclude(historical_period__end_date__lt=datetime.date.today())
    except Module.DoesNotExist:
        raise Http404
    return render_to_response(
        'modules/module_posts.html',
        {
            'module': module,
            'posts': posts,
        },
        RequestContext(request)
    )