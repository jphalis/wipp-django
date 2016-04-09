# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-03-20 15:56
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('reservation_status', models.IntegerField(choices=[(0, 'Pending'), (1, 'Negotiating'), (2, 'Accepted'), (3, 'Completed'), (4, 'Canceled')], default=0)),
                ('pick_up_interval', models.CharField(default='now', max_length=21)),
                ('start_amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=4)),
                ('final_amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=4)),
                ('start_query', models.CharField(blank=True, max_length=100, null=True)),
                ('destination_query', models.CharField(blank=True, max_length=100, null=True)),
                ('start_long', models.DecimalField(blank=True, decimal_places=8, max_digits=12, null=True)),
                ('start_lat', models.DecimalField(blank=True, decimal_places=8, max_digits=12, null=True)),
                ('end_long', models.DecimalField(decimal_places=8, max_digits=12, null=True)),
                ('end_lat', models.DecimalField(decimal_places=8, max_digits=12, null=True)),
                ('driver', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.Driver')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
