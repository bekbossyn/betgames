# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-25 16:28
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('game', '0014_warbets'),
    ]

    operations = [
        migrations.CreateModel(
            name='WarbetsLimit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('player_min', models.IntegerField(default=1)),
                ('player_max', models.IntegerField(default=20)),
                ('player_default', models.IntegerField(default=15)),
                ('player_count_till', models.IntegerField(default=30)),
                ('diller_min', models.IntegerField(default=1)),
                ('diller_max', models.IntegerField(default=20)),
                ('diller_default', models.IntegerField(default=15)),
                ('diller_count_till', models.IntegerField(default=30)),
                ('draw_min', models.IntegerField(default=1)),
                ('draw_max', models.IntegerField(default=20)),
                ('draw_default', models.IntegerField(default=15)),
                ('draw_count_till', models.IntegerField(default=30)),
                ('player_red_min', models.IntegerField(default=1)),
                ('player_red_max', models.IntegerField(default=20)),
                ('player_red_default', models.IntegerField(default=15)),
                ('player_red_count_till', models.IntegerField(default=30)),
                ('diller_red_min', models.IntegerField(default=1)),
                ('diller_red_max', models.IntegerField(default=20)),
                ('diller_red_default', models.IntegerField(default=15)),
                ('diller_red_count_till', models.IntegerField(default=30)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('active', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['active'],
            },
        ),
        migrations.CreateModel(
            name='WarbetsUserLimit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('one_pair', models.IntegerField(default=5)),
                ('one_pair_push', models.BooleanField(default=True)),
                ('two_pairs', models.IntegerField(default=5)),
                ('two_pairs_push', models.BooleanField(default=True)),
                ('three_of_a_kind', models.IntegerField(default=5)),
                ('three_of_a_kind_push', models.BooleanField(default=True)),
                ('flush', models.IntegerField(default=5)),
                ('flush_push', models.BooleanField(default=True)),
                ('straight', models.IntegerField(default=5)),
                ('straight_push', models.BooleanField(default=True)),
                ('full_house', models.IntegerField(default=5)),
                ('full_house_push', models.BooleanField(default=True)),
                ('four_of_a_kind', models.IntegerField(default=5)),
                ('four_of_a_kind_push', models.BooleanField(default=True)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='warbets',
            name='diller_black',
            field=models.BooleanField(db_index=True, default=False),
        ),
        migrations.AddField(
            model_name='warbets',
            name='player_black',
            field=models.BooleanField(db_index=True, default=False),
        ),
    ]
