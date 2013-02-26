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

import logging
logger = logging.getLogger(__name__)

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

# Stuff for dealing with sign-up and module information gathering.
from allauth.socialaccount.models import SocialToken
from allauth.account.signals import user_signed_up
import oauth2 as oauth

import xml.etree.ElementTree as ET
import re

import certifi

from accounts.models import StudentProfile, LecturerProfile
from modules.models import AcademicYear as Year
from modules.models import Module

def create_student_profile(user, modules, year):
    profile = StudentProfile()
    profile.user_profile = user.get_profile()
    db_modules = []
    for module in modules:
        try:
            m = Module.objects.filter(short_code__iexact=module)[0]
            db_modules.append(m)
        except IndexError:
            pass

    try:
        y = Year.objects.filter(short_code__iexact=year)[0]
        profile.year = y
    except IndexError:
        pass

    profile.save()

    profile.modules = db_modules

    return profile


def warwick_sign_up(sender, request, user, **kwargs):
    logger.debug('Getting module info for %s' % user.username)
    url = 'https://webgroups.warwick.ac.uk/query/user/%s/groups'
    regex = '%s-(.*)'
    try:
        socialtoken = SocialToken.objects.filter(account__user=user,
                                                 account__provider="warwick")[0]
        socialapp = socialtoken.app
        socialaccount = socialtoken.account
        extra_data = dict(socialaccount.extra_data)
    except (IndexError, ValueError):
        return

    token = oauth.Token(socialtoken.token, socialtoken.token_secret)
    consumer = oauth.Consumer(socialapp.client_id, socialapp.secret)

    client = oauth.Client(consumer, token)
    client.ca_certs = certifi.where()

    url = url % extra_data['user']

    resp, content = client.request(url)

    if resp['status'] == '200':
        root = ET.fromstring(content)
    else:
        logger.warning('Did not get 200 back from webgroups for %s. Got % ' % (
            socialaccount.user, resp))
        return

    modules = []

    for group in root.findall('group'):
        if group.find('type').text == "Module":
            dep_code = group.find('department').attrib['code']
            name = group.attrib['name']

            m = re.match(regex % dep_code, name).group(1)
            modules.append(m)

    year = extra_data['warwickyearofstudy']

    logger.debug('User %s: ')
    logger.debug('  Student: %s' % extra_data['student'])
    logger.debug('  Staff: %s' % extra_data['staff'])
    logger.debug('  Modules: %s' % modules)
    if extra_data['student'] == 'true':
        create_student_profile(user, modules, year)

    # if extra_data['staff# '] == 'true':
    #         LecturerProfile()

user_signed_up.connect(warwick_sign_up)
