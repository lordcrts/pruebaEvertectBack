"""Development settings."""

from .base import *  # NOQA
from .base import env

# Base
DEBUG = True

# Security
SECRET_KEY = env('DJANGO_SECRET_KEY', default='yt^*y36xx^xwa(4&gmx3gup7d2eb@(9)ic#8bwb=ea147zrc=5')
ALLOWED_HOSTS = [
    '*',
]

# Cache
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': ''
    }
}

# Templates
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG  # NOQA

# django-extensions
INSTALLED_APPS += ['django_extensions']  # noqa F405
