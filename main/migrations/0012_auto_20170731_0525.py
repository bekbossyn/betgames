# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-31 05:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_myuser_sound_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='sound_name',
            field=models.CharField(default='onesignal0', max_length=255),
        ),
    ]
