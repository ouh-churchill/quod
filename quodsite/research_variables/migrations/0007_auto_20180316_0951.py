# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-03-16 09:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('research_variables', '0006_auto_20180316_0912'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newvariable',
            name='category',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='newvariable',
            name='section',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='newvariable',
            name='version',
            field=models.PositiveIntegerField(),
        ),
    ]
