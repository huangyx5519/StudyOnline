# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-06-04 21:44
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='city',
            name='desc',
        ),
    ]
