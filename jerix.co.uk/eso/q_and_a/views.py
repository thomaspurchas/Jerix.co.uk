import json

from django.http import Http404, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template.defaultfilters import slugify
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required

from taggit.models import Tag

from q_and_a.models import Question, Answer
from modules.models import Module
# Create your views here.
def question(request, question_id, slug=None):
    question = get_object_or_404(
                                    Question.objects.select_related(),
                                    pk=question_id
    )

    if slug != question.slug:
        return redirect('question',
            question_id=question_id, slug=slugify(question.title),
            permanent=False)

    answers = question.answers.all()

    question.voted_down = question.has_down_voted(request.user)
    question.voted_up = question.has_up_voted(request.user)
    for answer in answers:
        answer.voted_down = answer.has_down_voted(request.user)
        answer.voted_up = answer.has_up_voted(request.user)

    return render_to_response(
        'q_and_a/question.html',
        {
            'question': question,
            'answers': answers
        },
        RequestContext(request)
    )

def tagged(request, tag):
    tag = get_object_or_404(Tag, slug=tag)
    question_list = Question.objects.filter(tags=tag)

    per_page = request.GET.get('per_page')
    try:
        per_page = int(per_page)
        if per_page in [15, 30, 50]:
            request.session['per_page'] = per_page
    except (ValueError, TypeError):
        per_page = request.session.get('per_page', 15)

    paginator = Paginator(question_list, per_page)

    page = request.GET.get('page')
    try:
        questions = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        questions = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        questions = paginator.page(paginator.num_pages)

    return render_to_response(
        'q_and_a/list.html',
        {
            'questions': questions,
            'page': page,
            'per_page': per_page,
            'tag': tag.name
        },
        RequestContext(request)
    )

@login_required
def vote(request):
    if request.method == 'POST' and request.is_ajax():
        user = request.user
        print request.raw_post_data
        ob_type = request.POST.get('type')
        pk = request.POST.get('id')
        vote = request.POST.get('vote')
        clear = True if request.POST.get('clear') == 'true' else False

        if ob_type == 'question':
            ob = get_object_or_404(Question, pk=pk) # Should be a 422 error
        elif ob_type == 'answer':
            ob = get_object_or_404(Answer, pk=pk) # Same as above

        response_data = None
        if clear:
            print 'Clear vote'
            ob.clear_vote(user)
            response_data = {
                'votes': ob.current_vote
            }
        else:
            if vote == 'up':
                ob.vote_up(user)
                response_data = {
                    'votes': ob.current_vote
                }
            elif vote == 'down':
                ob.vote_down(user)
                response_data = {
                    'votes': ob.current_vote
                }

        if response_data:
            return HttpResponse(
                                json.dumps(response_data),
                                mimetype="application/json",
                                status=200
            )

    return HttpResponse(status=400)