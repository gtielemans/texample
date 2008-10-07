# Django settings for testresources project.

import os
from os.path import join,basename,splitext,normpath

from os import path as os_path
PROJECT_PATH = os_path.abspath(os_path.split(__file__)[0])



DEBUG = True

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

DATABASE_ENGINE = 'sqlite3'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = os_path.join(PROJECT_PATH,'texample.sqlite')             # Or path to database file if using sqlite3.
DATABASE_USER = ''             # Not used with sqlite3.
DATABASE_PASSWORD = ''         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'your secret key'


# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'CET'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"

if DEBUG:
    MEDIA_URL = '/media/'
else:
    MEDIA_URL = 'http://media.texample.net/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/adminmedia/'



# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.doc.XViewMiddleware',
    
)

ROOT_URLCONF = 'texample.urls'


MARKUP_FILTER = ('markdown', {'safe_mode': False,
                              'extensions' :['headerid(level=3)','codehilite']})

MARKUP_SETTINGS = {
    'markdown' : {'safe_mode': False,
                  'extensions' :['codehilite(css_class=highlight)']},
    'restructuredtext' : {'settings_overrides' : {'initial_header_level': 2}},
}


TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os_path.join(PROJECT_PATH, 'templates'),
    os_path.join(PROJECT_PATH, 'templates/tikz'),
)


GENERIC_CONTENT_LOOKUP_KWARGS = {
        'texblog.entry': { 'draft': False }
    }


INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    # Third party apps
    'django_evolution',
    'template_utils',
    'django_extensions',
    'contact_form',
    'tagging',
    'typogrify',
    # Texample apps
    'texpubutils',
    'texample.tikz',
    'pkgbuilds',
    'pkgresources',
    'texample.aggregator',
    'ganalytics',
    'texarticles',
    'texblog',
    'texgallery',
    'utils',
        
)

try:
    # Load database and secret key and debug settings
    from texample.current_settings import *
    try:
        MIDDLEWARE_CLASSES = MIDDLEWARE_CLASSES + dbgMIDDLEWARE_CLASSES
        INSTALLED_APPS = INSTALLED_APPS + dbgINSTALLED_APPS
    except:
        pass
except:
    raise
    pass

TEMPLATE_DEBUG = DEBUG
MANAGERS = ADMINS

# in settings.py

GALLERY_URL = MEDIA_URL + 'tikz/examples/'
#auth, debug and i18n 
TEMPLATE_CONTEXT_PROCESSORS = (
    # defaults
    "django.core.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.media",
    "utils.context_processors.settings.GALLERY_URL",
    
)