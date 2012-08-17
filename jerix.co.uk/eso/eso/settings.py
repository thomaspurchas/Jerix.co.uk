import os
import djcelery
# Django settings for eso project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Thomas Purchas', 'thomas@jerix.co.uk'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'db.sqlite',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Celery
djcelery.setup_loader()
BROKER_URL = 'django://'

# Haystack
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.simple_backend.SimpleEngine',
    },
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/London'

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
MEDIA_ROOT = '%s/media/' % SITE_ROOT

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = '%s/static/' % SITE_ROOT

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

STATIC_DOC_ROOT = '%s/static/' % SITE_ROOT

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    '%s/core_static/' % SITE_ROOT,
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
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
    'haystack',
    'south',
    'tastypie',
    'gunicorn',
    'celery_haystack',
    'cumulus',
    'djcelery',
    #'djcelery.transport',

    # My Apps
    'modules',
    'search',
    'store',
    'accounts',
    'files',
    'students',
    'reputation',
    'q_and_a',
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
    },
    'loggers': {
        '': {
            'handlers':['console'],
            'propagate': True,
            'level':'DEBUG',
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
    }
}

FILE_TYPE_MAPPINGS = {
    "(?i).*\.pdf$": {
        "type": "pdf",
        "path": "DerivedPDFs:",
    },
    "(?i).*\.png$": {
        "type": "png",
        "path": "DerivedPNGs:",
    },
    "(?i).*\.docx?$": {
        "type": "word",
        "path": None,
    },
    "(?i).*\.(pptx?|ppts?)$": {
        "type": "slide",
        "path": None,
    },
}

PARENT_BLOBS_CONTAINER = 'ParentBlobs'

CUMULUS = {
    'API_KEY': '',
    'AUTH_URL': 'uk_authurl',
    'CNAMES': None,
    'CONTAINERS': {
        'uploads': False,
        PARENT_BLOBS_CONTAINER: False,
        'DerivedPDFs': False,
        'DerivedPNGs': True,
    },
    'DEFAULT_CONTAINER': 'uploads',
    'SERVICENET': False,
    'TIMEOUT': 5,
    'TTL': 600,
    'USE_SSL': False,
    'USERNAME': '',
    'STATIC_CONTAINER': None,
    'FILTER_LIST': []
}

if not DEBUG:
    DEFAULT_FILE_STORAGE = 'cumulus.storage.CloudFilesStorage'

try:
    from local_settings import *
    CUMULUS.update({
        'API_KEY': CLOUDFILES_API_KEY,
        'USERNAME': CLOUDFILES_USERNAME
    })
except:
    pass
