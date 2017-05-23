import os
from whitenoise.django import DjangoWhiteNoise
from django.core.wsgi import get_wsgi_application

os.environ['DJANGO_SETTINGS_MODULE'] = 'auxbox.settings'

application = get_wsgi_application()
application = DjangoWhiteNoise(application)
