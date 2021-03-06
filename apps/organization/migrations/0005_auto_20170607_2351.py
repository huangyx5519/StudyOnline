# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-06-07 23:51
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0004_auto_20170605_1652'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='teacher',
            name='age',
        ),
        migrations.AlterField(
            model_name='teacher',
            name='organization',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='organization.CourseOrganization', verbose_name='\u6240\u5c5e\u673a\u6784'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='points',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='\u6559\u5b66\u7279\u70b9'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='work_company',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='\u5c31\u804c\u516c\u53f8'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='work_position',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='\u516c\u53f8\u804c\u4f4d'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='work_years',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='\u5de5\u4f5c\u5e74\u9650'),
        ),
    ]
