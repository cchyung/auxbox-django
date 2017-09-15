from auxbox.settings.base import *


DEBUG = True

INSTALLED_APPS += [
    'django_extensions',
    'django_twilio',
]

ALLOWED_HOSTS += [
    '*'
]



# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'auxbox_dev',
        'USER': 'Drew',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '5432'
    }
}
