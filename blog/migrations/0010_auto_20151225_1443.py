# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-25 06:43
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nineku', '0009_auto_20151225_1420'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dreamdb',
            name='datetime',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 25, 14, 43, 25, 787797)),
        ),
        migrations.AlterField(
            model_name='likes',
            name='user',
            field=models.CharField(max_length=100),
        ),
    ]
