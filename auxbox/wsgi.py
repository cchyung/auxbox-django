import os
from whitenoise.django import DjangoWhiteNoise
from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
application = DjangoWhiteNoise(application)
