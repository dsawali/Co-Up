# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-01 09:25
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('conversations', '0002_auto_20171126_0012'),
    ]

    operations = [
        migrations.AddField(
            model_name='conversation',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='conversation',
            name='modified',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='group',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='group',
            name='modified',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
