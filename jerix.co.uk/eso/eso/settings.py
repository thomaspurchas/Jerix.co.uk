import os
from os.path import join as pathjoin
import djcelery
from memcache import MEMCACHE
# Django settings for eso project.

DEBUG = os.environ.get('DEBUG', "true").lower() == "true"
TEMPLATE_DEBUG = os.environ.get('TEMPLATE_DEBUG', "true").lower() == "true"
STAGING = os.environ.get('STAGING', "false").lower() == "true"
#DEBUG = False

ADMINS = (
    ('Thomas Purchas', 'thomas@jerix.co.uk'),
)

MANAGERS = ADMINS

LOGIN_URL = 'account/login/'

if not DEBUG:
    CACHES = {
        'default': MEMCACHE
    }
else:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        }
    }

import dj_database_url
DATABASES = {'default': dj_database_url.config(default='postgres://localhost/jerix_heroku')}

# Celery
djcelery.setup_loader()
BROKER_URL = os.environ.get('CLOUDAMQP_URL', 'amqp://app8750632_heroku.com:EauSZ0LugIDHW90x-aUqtUcnwurBusiG@tiger.cloudamqp.com/app8750632_heroku.com')#'django://')
BROKER_POOL_LIMIT = 1

# Haystack
HAYSTACK_URL      = os.environ.get('HAYSTACK_URL', 'http://localhost:8983/solr') #'https://secure.websolr.com/solr/86a571d1d3f')
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
        'URL': HAYSTACK_URL,
    },
}


# Hitcount app
HITCOUNT_KEEP_HIT_ACTIVE = { 'days': 2 }
HITCOUNT_HITS_PER_IP_LIMIT = 0
#HITCOUNT_EXCLUDE_USER_GROUP = ( 'Editor', )

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/London'

DATE_FORMAT = "N j Y"
TIME_FORMAT = "g:i a"

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-GB'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Useful SITE_ROOT variable
SITE_ROOT = '/'.join(os.path.dirname(__file__).split('/')[0:-2])

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = pathjoin(SITE_ROOT, 'media/')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '//media.dev.jerix.co.uk' if DEBUG else '//media.jerix.co.uk/'
if STAGING:
    MEDIA_URL = '//media.dev.jerix.co.uk/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = pathjoin(SITE_ROOT, 'static/')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/' if DEBUG else '//static.jerix.co.uk/'
if STAGING:
    STATIC_URL = '//staticdev.jerix.co.uk/'

STATIC_DOC_ROOT = pathjoin(SITE_ROOT, 'static/')

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    pathjoin(SITE_ROOT, 'core_static/'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'ew#f7r0^#1=29n7h!3jh@g6*6^+*&amp;k6alz0mm8rbn#t)^mt-5j'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
  "django.contrib.auth.context_processors.auth",
  "django.core.context_processors.debug",
  "django.core.context_processors.i18n",
  "django.core.context_processors.media",
  "django.core.context_processors.static",
  "django.core.context_processors.tz",
  "django.contrib.messages.context_processors.messages",
  'django.core.context_processors.request',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'eso.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'eso.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    '%s/eso/templates' % SITE_ROOT,
)

# Use the BCrypt password hash
PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.BCryptPasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
)

# Set user profile model
AUTH_PROFILE_MODULE = 'accounts.UserProfile'

SESSION_ENGINE = "django.contrib.sessions.backends.cached_db"

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    'django.contrib.admindocs',

    # Utility apps
    'django.contrib.markup',
    'haystack',
    'south',
    'tastypie',
    'gunicorn',
    'celery_haystack',
    'djcelery',
    'storages',
    'hitcount',
    'taggit',
    'compressor',
    'raven.contrib.django',
    'kombu.transport.django',
    'celery_haystack',
    'crispy_forms',

    # My Apps
    'modules',
    'search',
    'store',
    'accounts',
    'files',
    'students',
    'reputation',
    'q_and_a',
    'pagedown',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(name)s %(lineno)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
            'level':'DEBUG',
            'class':'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'sentry': {
            'level': 'ERROR',
            'class': 'raven.contrib.django.handlers.SentryHandler',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        '': {
            'handlers':['console', 'sentry'],
            'propagate': True,
            'level':'DEBUG' if DEBUG else 'INFO',
        },
        'django': {
            'handlers':['console'],
            'propagate': False,
            'level':'INFO',
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'sentry.errors': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
        'newrelic': {
            'propagate': False,
            'handlers': ['console'],
            'level': 'ERROR'
        },
        'boto': {
            'propagate': False,
            'handers': ['console', 'sentry'],
            'level': 'INFO'
        }
    }
}

if DEBUG:
    LOGGING['loggers']['newrelic'] = {
        'handers': [],
        'level': 'DEBUG',
        'propagate': False,
    }

FILE_TYPE_MAPPINGS = {
    "(?i).*\.pdf$": {
        "type": "pdf",
        "display": "PDF",
        "priority": 99,
        "path": "DerivedPDFs/",
    },
    "(?i).*\.png$": {
        "type": "png",
        "path": "DerivedPNGs/",
    },
    "(?i).*\.docx?$": {
        "type": "word",
        "display": "Doc",
        "path": None,
    },
    "(?i).*\.(pptx?|ppts?|pptm)$": {
        "type": "slide",
        "display": "Powerpoint",
        "path": None,
    },
}

PARENT_BLOBS_LOCATION = 'ParentBlobs/'

from boto.s3.connection import VHostCallingFormat

AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_DEFAULT_ACL = 'authenticated-read'
AWS_STORAGE_BUCKET_NAME = 'media.dev.jerix.co.uk' if DEBUG else 'media.jerix.co.uk'
AWS_QUERYSTRING_AUTH = False
AWS_S3_CUSTOM_DOMAIN = 'media.dev.jerix.co.uk' if DEBUG else 'media.jerix.co.uk'
AWS_S3_CALLING_FORMAT = VHostCallingFormat()
if not DEBUG:
    STATICFILES_STORAGE = 'eso.static_storage.StaticStorage'
    COMPRESS_STORAGE = STATICFILES_STORAGE
if STAGING:
    AWS_STORAGE_BUCKET_NAME = 'media.dev.jerix.co.uk'
    AWS_S3_CUSTOM_DOMAIN = 'media.dev.jerix.co.uk'
    STATICFILES_STORAGE = 'eso.static_storage.StaticStorage'
    COMPRESS_STORAGE = STATICFILES_STORAGE

# Enable offline compression
COMPRESS_ENABLED = True
COMPRESS_OFFLINE = (not DEBUG) or STAGING
COMPRESS_URL = STATIC_URL
COMPRESS_CSS_FILTERS = [
    'compressor.filters.css_default.CssAbsoluteFilter',
    #'compressor.filters.csstidy.CSSTidyFilter',
]
COMPRESS_PRECOMPILERS = [
    ('text/less', 'lessc {infile} {outfile}'),
    ('text/x-sass', 'sass {infile} {outfile}'),
    ('text/x-scss', 'sass --scss {infile} {outfile}'),
]

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
