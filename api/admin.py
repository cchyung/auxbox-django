# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from .models import Track, Session

# Register your models here.
admin.site.register(Session)
admin.site.register(Track)
