# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-18 10:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0002_auto_20160118_1027'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='is_accepted',
            field=models.BooleanField(default=False, verbose_name='accepted'),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='active'),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='is_completed',
            field=models.BooleanField(default=False, verbose_name='completed'),
        ),
    ]
