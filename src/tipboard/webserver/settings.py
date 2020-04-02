import os
from src.tipboard.app.properties import SUPER_SECRET_KEY, DEBUG, REDIS_HOST, REDIS_PORT, PATH_FOR_PIP

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'channels',
    PATH_FOR_PIP + 'tipboard.app.Config',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.BrokenLinkEmailsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
]

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = SUPER_SECRET_KEY
DEBUG = DEBUG
ALLOWED_HOSTS = ['*']
TIME_ZONE = 'Europe/Paris'
USE_TZ = True
ROOT_URLCONF = PATH_FOR_PIP + 'tipboard.webserver.urls'
WSGI_APPLICATION = PATH_FOR_PIP + 'tipboard.webserver.wsgi.application'
ASGI_APPLICATION = PATH_FOR_PIP + 'tipboard.webserver.routing.application'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR + '/templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'libraries': {
                'template_filter': PATH_FOR_PIP + 'tipboard.templates.template_filter',
            }
        },
    },
]

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

STATIC_URL = '/static/'

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [(REDIS_HOST, REDIS_PORT)],
        },
    }
}
