from .settings import *

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = [
    'django-template.bekonline.webfactional.com',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': '',
        'PORT': '',
        'NAME': 'django_template',
        'USER': 'django_template',
        'PASSWORD': 'yepR7fRuXebAdRaphurU2uB6StuSWa2r',
    }
}

STATIC_ROOT = '/home/bekonline/webapps/django_template_static/static/'
STATIC_URL = 'http://django-template.bekonline.webfactional.com/static/static/'

MEDIA_ROOT = '/home/bekonline/webapps/django_template_static/media/'
MEDIA_URL = 'http://django-template.bekonline.webfactional.com/static/media/'

