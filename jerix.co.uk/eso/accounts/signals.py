# Stuff for dealing with sign-up and module information gathering.
from allauth.socialaccount.models import SocialToken
from allauth.account.signals import user_signed_up
import oauth2 as oauth

import xml.etree.ElementTree as ET
import re

import certifi

from accounts.models import StudentProfile
from modules.models import AcademicYear as Year
from modules.models import Module

import logging
logger = logging.getLogger(__name__)

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
    logger.info('Getting module info for %s' % user.username)
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

    logger.info('User %s: ')
    logger.info('  Student: %s' % extra_data['student'])
    logger.info('  Staff: %s' % extra_data['staff'])
    logger.info('  Modules: %s' % modules)
    if extra_data['student'] == 'true':
        create_student_profile(user, modules, year)

    # if extra_data['staff# '] == 'true':
    #         LecturerProfile()

user_signed_up.connect(warwick_sign_up)
