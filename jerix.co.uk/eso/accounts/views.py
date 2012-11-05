from urlparse import urlparse, urlunparse

from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.cache import never_cache
from django.utils.cache import patch_cache_control

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
    redirect = request.REQUEST.get('next')

    if not redirect:
        redirect = settings.LOGIN_REDIRECT_URL

    netloc = urlparse(redirect)[1]
    # Heavier security check -- don't allow redirection to a different
    # host.
    if netloc and netloc != request.get_host():
        redirect = settings.LOGIN_REDIRECT_URL

    if request.user.is_authenticated():
        return HttpResponseRedirect(redirect)

    print 'Method:', request.method
    print 'Redirect:', redirect
    print 'session id:', request.session.session_key

    if request.method == "POST":
        if request.POST.get('login_universal') == "true":
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
        print 'is_valid', form.is_valid()
        if form.is_valid():

            auth_login(request, form.get_user())

            if request.session.test_cookie_worked():
                print 'test cookie worked'
                request.session.delete_test_cookie()

            if not form.cleaned_data['remember_me']:
                print 'No remember_me'
                request.session.set_expiry(0)

            response =  HttpResponseRedirect(redirect)
            # Manual cache header fiddling to help prevent caching issues.
            patch_cache_control(response, no_cache=True, no_store=True, must_revalidate=True)
            print 'response:', response
            return response
    else:
        form = AuthForm(request)

    #request.session.set_test_cookie()

    context = {
        'form': form,
        'next': redirect,
    }

    response = render(request, 'registration/login.html', context)
    # Manual cache header fiddling to help prevent caching issues.
    patch_cache_control(response, no_cache=True, no_store=True, must_revalidate=True)
    return response