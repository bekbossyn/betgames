# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-15 14:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BaccaratLimit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('player_min', models.IntegerField(default=3)),
                ('player_max', models.IntegerField(default=3)),
                ('banker_min', models.IntegerField(default=3)),
                ('banker_max', models.IntegerField(default=3)),
                ('tie_min', models.IntegerField(default=3)),
                ('tie_max', models.IntegerField(default=3)),
                ('either_pair_min', models.IntegerField(default=3)),
                ('either_pair_max', models.IntegerField(default=3)),
                ('big_min', models.IntegerField(default=3)),
                ('big_max', models.IntegerField(default=3)),
                ('small_min', models.IntegerField(default=3)),
                ('small_max', models.IntegerField(default=3)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('active', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['active'],
            },
        ),
    ]
