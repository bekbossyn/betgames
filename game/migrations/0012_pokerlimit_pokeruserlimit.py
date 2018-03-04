# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-07 10:58
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('game', '0011_poker_four_of_a_kind'),
    ]

    operations = [
        migrations.CreateModel(
            name='PokerLimit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('one_pair_min', models.IntegerField(default=1)),
                ('one_pair_max', models.IntegerField(default=20)),
                ('one_pair_default', models.IntegerField(default=15)),
                ('one_pair_count_till', models.IntegerField(default=30)),
                ('two_pairs_min', models.IntegerField(default=1)),
                ('two_pairs_max', models.IntegerField(default=20)),
                ('two_pairs_default', models.IntegerField(default=15)),
                ('two_pairs_count_till', models.IntegerField(default=30)),
                ('three_of_a_kind_min', models.IntegerField(default=1)),
                ('three_of_a_kind_max', models.IntegerField(default=20)),
                ('three_of_a_kind_default', models.IntegerField(default=15)),
                ('three_of_a_kind_count_till', models.IntegerField(default=30)),
                ('flush_min', models.IntegerField(default=1)),
                ('flush_max', models.IntegerField(default=20)),
                ('flush_default', models.IntegerField(default=15)),
                ('flush_count_till', models.IntegerField(default=30)),
                ('straight_min', models.IntegerField(default=1)),
                ('straight_max', models.IntegerField(default=20)),
                ('straight_default', models.IntegerField(default=15)),
                ('straight_count_till', models.IntegerField(default=30)),
                ('full_house_min', models.IntegerField(default=1)),
                ('full_house_max', models.IntegerField(default=20)),
                ('full_house_default', models.IntegerField(default=15)),
                ('full_house_count_till', models.IntegerField(default=30)),
                ('four_of_a_kind_min', models.IntegerField(default=1)),
                ('four_of_a_kind_max', models.IntegerField(default=20)),
                ('four_of_a_kind_default', models.IntegerField(default=15)),
                ('four_of_a_kind_count_till', models.IntegerField(default=30)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('active', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['active'],
            },
        ),
        migrations.CreateModel(
            name='PokerUserLimit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('one_pair', models.IntegerField(default=5)),
                ('two_pairs', models.IntegerField(default=5)),
                ('three_of_a_kind', models.IntegerField(default=5)),
                ('flush', models.IntegerField(default=5)),
                ('straight', models.IntegerField(default=5)),
                ('full_house', models.IntegerField(default=5)),
                ('four_of_a_kind', models.IntegerField(default=5)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
