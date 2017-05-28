from __future__ import unicode_literals
from django.db import models

class Session(models.Model):
    owner = models.ForeignKey('auth.User', help_text='Owner', default=None)
    name = models.CharField(max_length=50, default = 'Default Session')

    def __str__(self):
        return self.name

class Track(models.Model):
    session = models.ForeignKey('api.Session', help_text='Session')
    title = models.CharField(max_length=50, help_text='Track Title', default='Default Track')
    url = models.URLField()

    def __str__(self):
        return self.url
