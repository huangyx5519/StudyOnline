# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-06-07 22:58
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0004_auto_20170605_1652'),
        ('users', '0003_banner_emailverifyrecord'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='teacher_role',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='organization.Teacher', verbose_name='\u6559\u5e08id'),
        ),
    ]
