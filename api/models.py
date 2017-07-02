from __future__ import unicode_literals
import uuid
from django.db import models
from django.template.defaultfilters import slugify


class Session(models.Model):
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey('auth.User', related_name='sessions', help_text='Owner', default=None)
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
    title = models.CharField(max_length=50, help_text='Track Title', default='Default Track')
    track_id = models.CharField(max_length=20, help_text='Spotify Track ID', default='')

    def __str__(self):
        return self.title
