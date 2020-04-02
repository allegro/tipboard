import os
from src.tipboard.app.properties import API_KEY, DEBUG, REDIS_HOST, REDIS_PORT, PATH_FOR_PIP

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
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.BrokenLinkEmailsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
]

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = API_KEY
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
# local directory where to find the static ressources
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static/'), ]
# local directory where all statics ressources will be regrouped (in prod mode this file are on a CDN)
STATIC_ROOT = os.path.join(BASE_DIR, 'collectTestStatic/')
STATIC_URL = '/static/'  # Url asked by the client to get the static ressources by HTTP

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [(REDIS_HOST, REDIS_PORT)],
        },
    }
}
