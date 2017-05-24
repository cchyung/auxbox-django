from .base import *
import dj_database_url

DATABASES['default'] =  dj_database_url.config()

SECRET_KEY = '=w@ualtox7^w203!+^inc*f8z+#e3*2zs7%vjv4qw0rqc$yy@0'
