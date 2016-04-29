# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-04-28 00:43
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('reservations', '0004_auto_20160408_2019'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='pending_drivers',
            field=models.ManyToManyField(blank=True, related_name='pending_drivers', to=settings.AUTH_USER_MODEL),
        ),
    ]