from auxbox.settings.base import *

DEBUG = True

INSTALLED_APPS += [
    'django_extensions'
]

ALLOWED_HOSTS += [
    u'localhost',
]


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'auxbox_dev',
        'USER': 'conner',
        'PASSWORD': 'developer',
        'HOST': 'localhost',
        'PORT': '5432'
    }
}
