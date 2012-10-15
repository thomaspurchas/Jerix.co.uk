from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404, render_to_response

# Create your views here.
def login_user(request):
    return HttpResponse('Getting there slowly')