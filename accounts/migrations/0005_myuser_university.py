# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-04-27 18:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20160411_2335'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='university',
            field=models.CharField(blank=True, max_length=180),
        ),
    ]