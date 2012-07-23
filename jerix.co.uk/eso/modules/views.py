from django.http import Http404
from django.template import RequestContext
from django.shortcuts import render_to_response

from modules.models import Module
# Create your views here.
def module_detail(request, module_id):
    try:
        module = Module.objects.get(pk=module_id)
    except Module.DoesNotExist:
        raise Http404
    return render_to_response('modules/module.html', {'module': module}, RequestContext(request))