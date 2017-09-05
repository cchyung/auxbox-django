from __future__ import unicode_literals
import uuid
from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user')
    spotify_refresh_token = models.CharField(default='', max_length=100)
    spotify_access_token = models.CharField(default='', max_length=100)
    def __str__(self):
        return self.user.username


class Session(models.Model):
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey('Profile', related_name='sessions', help_text='Owner', default=None)
    name = models.CharField(max_length=50, default = 'Default Session')
    slug = models.SlugField(default = 'default-session')

    class Meta:
        unique_together = ('owner', 'name')

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Session, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Track(models.Model):
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    session = models.ForeignKey('api.Session', related_name='tracks', help_text='Session')
    track_id = models.CharField(max_length=20, help_text='Spotify Track ID', default='')

    def __str__(self):
        return self.title
