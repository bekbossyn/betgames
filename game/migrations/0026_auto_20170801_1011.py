# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-08-01 10:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0025_cache'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cache',
            name='name',
            field=models.CharField(db_index=True, max_length=2555, unique=True),
        ),
        migrations.AlterField(
            model_name='cache',
            name='new',
            field=models.BooleanField(db_index=True, default=True),
        ),
    ]
