import datetime

from django.http import Http404
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.db.models import Q

from modules.models import Module
# Create your views here.
def module_detail(request, module_id):
    try:
        module = Module.objects.get(pk=module_id)
        posts = module.posts.filter(
            Q(historical_period__start_date__lt=datetime.date.today()) |
            Q(historical_period=None)
        )
        print posts
        posts = posts.exclude(historical_period__end_date__lt=datetime.date.today())
        print posts
    except Module.DoesNotExist:
        raise Http404
    return render_to_response(
        'modules/module.html',
        {
            'module': module,
            'posts': posts,
        },
        RequestContext(request)
    )