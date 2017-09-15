from __future__ import unicode_literals
import uuid
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.template.defaultfilters import slugify


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)

        user = self.model(
            email=email,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        user = self.create_user(email, password, **extra_fields)
        user.is_admin = True

        user.save(using=self._db)
        return user



class User(AbstractUser):
    username = models.CharField(null = True, max_length=1)
    email = models.EmailField(unique=True)
    spotify_refresh_token = models.CharField(default='', max_length=100, blank=True)
    spotify_access_token = models.CharField(default='', max_length=100, blank=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'


class Anon(models.Model):
    phone = models.CharField(max_length=25)
    added_date = models.DateTimeField()  #Used to remove old anon users to clean the table
    joined_session = models.CharField(max_length=100)


class Session(models.Model):
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey('api.User', related_name='sessions', help_text='Owner', default=None)
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
