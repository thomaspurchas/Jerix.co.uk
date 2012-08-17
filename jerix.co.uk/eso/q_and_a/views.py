from django.http import Http404
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from django.template.defaultfilters import slugify

from q_and_a.models import Question
from modules.models import Module
# Create your views here.
def module_q_and_a(request, module_id, slug=None):
    try:
        module = Module.objects.get(pk=module_id)
        if slug != slugify(module.title):
            return redirect('module-qa',
                module_id=module_id, slug=slugify(module.title),
                permanent=False)
        questions = Question.objects.filter(module=module)
    except Module.DoesNotExist:
        raise Http404
    return render_to_response(
        'modules/module_qa.html',
        {
            'module': module,
            'questions': questions,
        },
        RequestContext(request)
    )