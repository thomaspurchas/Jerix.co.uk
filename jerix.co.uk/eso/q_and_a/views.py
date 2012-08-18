from django.http import Http404
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect, get_object_or_404
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

def question(request, question_id, slug=None):
    question = get_object_or_404(Question, pk=question_id)

    if slug != slugify(question.title):
        return redirect('question',
            question_id=question_id, slug=slugify(question.title),
            permanent=False)

    answers = question.answers.all()

    return render_to_response(
        'q_and_a/question.html',
        {
            'question': question,
            'answers': answers
        },
        RequestContext(request)
    )