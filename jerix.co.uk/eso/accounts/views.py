from urlparse import urlparse, urlunparse

from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.cache import never_cache

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, get_object_or_404, render
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login
from django.conf import settings

class AuthForm(AuthenticationForm):
    remember_me = forms.BooleanField(label="Remember Me", required=False, initial=True)

# Create your views here.
@sensitive_post_parameters()
@never_cache
def login_user(request):
    if request.method == "POST":
        if request.POST.get('login_universal') == "true":
            redirect = request.POST.get('next')
            username = request.POST.get('login_username')
            password = request.POST.get('login_password')
            remember = request.POST.get('login_remember_me')

            data = {
                'username': username,
                'password': password,
                'remember_me': remember,
            }

            form = AuthForm(data=data)
        else:
            form = AuthForm(data=request.POST)
            redirect = request.GET.get('next')

        if form.is_valid():
            if not redirect:
                redirect = settings.LOGIN_REDIRECT_URL

            netloc = urlparse(redirect)[1]
            # Heavier security check -- don't allow redirection to a different
            # host.
            if netloc and netloc != request.get_host():
                redirect = settings.LOGIN_REDIRECT_URL

            auth_login(request, form.get_user())

            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()

            if not form.cleaned_data['remember_me']:
                request.session.set_expiry(0)

            return HttpResponseRedirect(redirect)
    else:
        form = AuthForm(request)

    request.session.set_test_cookie()

    context = {
        'form': form,
    }

    return render(request, 'registration/login.html', context)

    return HttpResponse('Getting there slowly')