# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-06-08 16:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0006_auto_20170608_1615'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='work_position',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='\u516c\u53f8\u804c\u4f4d'),
        ),
        migrations.AddField(
            model_name='teacher',
            name='work_years',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='\u5de5\u4f5c\u5e74\u9650'),
        ),
    ]
