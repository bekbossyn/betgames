# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-20 12:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0002_baccaratlimit'),
    ]

    operations = [
        migrations.AddField(
            model_name='baccarat',
            name='banker_current',
            field=models.IntegerField(default=-1),
        ),
        migrations.AddField(
            model_name='baccarat',
            name='big_current',
            field=models.IntegerField(default=-1),
        ),
        migrations.AddField(
            model_name='baccarat',
            name='either_pair_current',
            field=models.IntegerField(default=-1),
        ),
        migrations.AddField(
            model_name='baccarat',
            name='player_current',
            field=models.IntegerField(default=-1),
        ),
        migrations.AddField(
            model_name='baccarat',
            name='small_current',
            field=models.IntegerField(default=-1),
        ),
        migrations.AddField(
            model_name='baccarat',
            name='tie_current',
            field=models.IntegerField(default=-1),
        ),
    ]
