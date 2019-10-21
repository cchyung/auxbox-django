# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-18 23:13
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20170610_1856'),
    ]

    operations = [
        migrations.AddField(
            model_name='session',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
    ]