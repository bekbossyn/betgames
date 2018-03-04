# -*- coding: utf-8 -*-
import random

from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models


class Baccarat(models.Model):
    uuid = models.CharField(max_length=15, unique=True, db_index=True)

    player = models.BooleanField(default=False, db_index=True)

    banker = models.BooleanField(default=False, db_index=True)

    tie = models.BooleanField(default=False, db_index=True)

    either_pair = models.BooleanField(default=False, db_index=True)

    big = models.BooleanField(default=False, db_index=True)

    small = models.BooleanField(default=False, db_index=True)

    timestamp = models.DateTimeField(blank=False, null=False, db_index=True)

    raw_result = models.CharField(max_length=255)

    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']


class Poker(models.Model):
    uuid = models.CharField(max_length=15, unique=True, db_index=True)

    one_pair = models.BooleanField(default=False, db_index=True)

    two_pairs = models.BooleanField(default=False, db_index=True)

    three_of_a_kind = models.BooleanField(default=False, db_index=True)

    four_of_a_kind = models.BooleanField(default=False, db_index=True)

    straight = models.BooleanField(default=False, db_index=True)

    flush = models.BooleanField(default=False, db_index=True)

    full_house = models.BooleanField(default=False, db_index=True)

    hand = models.CharField(max_length=25, default='1', db_index=True)

    timestamp = models.DateTimeField(blank=False, null=False, db_index=True)

    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']


class BaccaratLimitManager(models.Manager):

    def get_default(self):
        try:
            limit = BaccaratLimit.objects.filter(active=True)[0]
        except:
            limit = BaccaratLimit.objects.create(active=True)
        return limit


class BaccaratLimit(models.Model):
    player_min = models.IntegerField(default=1)
    player_max = models.IntegerField(default=20)

    player_default = models.IntegerField(default=15)

    player_count_till = models.IntegerField(default=30)

    banker_min = models.IntegerField(default=1)
    banker_max = models.IntegerField(default=20)

    banker_default = models.IntegerField(default=15)

    banker_count_till = models.IntegerField(default=30)

    tie_min = models.IntegerField(default=1)
    tie_max = models.IntegerField(default=60)

    tie_default = models.IntegerField(default=48)

    tie_count_till = models.IntegerField(default=100)

    either_pair_min = models.IntegerField(default=1)
    either_pair_max = models.IntegerField(default=65)

    either_pair_default = models.IntegerField(default=25)

    either_pair_count_till = models.IntegerField(default=100)

    big_min = models.IntegerField(default=1)
    big_max = models.IntegerField(default=20)

    big_default = models.IntegerField(default=12)

    big_count_till = models.IntegerField(default=30)

    small_min = models.IntegerField(default=1)
    small_max = models.IntegerField(default=20)

    small_default = models.IntegerField(default=12)

    small_count_till = models.IntegerField(default=30)

    created_time = models.DateTimeField(auto_now_add=True)

    active = models.BooleanField(default=False)

    objects = BaccaratLimitManager()

    def json(self):
        return {
            "player_min": self.player_min,
            "player_max": self.player_max,
            "banker_min": self.banker_min,
            "banker_max": self.banker_max,
            "tie_min": self.tie_min,
            "tie_max": self.tie_max,
            "either_pair_min": self.either_pair_min,
            "either_pair_max": self.either_pair_max,
            "big_min": self.big_min,
            "big_max": self.big_max,
            "small_min": self.small_min,
            "small_max": self.small_max
        }

    class Meta:
        ordering = ['active']


class BaccaratUserLimitManager(models.Manager):

    def get_default(self, user):
        try:
            limit = BaccaratUserLimit.objects.filter(user=user)[0]
        except:
            limit, _ = BaccaratUserLimit.objects.get_or_create(user=user)
            base_limit = BaccaratLimit.objects.get_default()
            limit.player = base_limit.player_default
            limit.banker = base_limit.banker_default
            limit.tie = base_limit.tie_default
            limit.big = base_limit.big_default
            limit.small = base_limit.small_default
            limit.either_pair = base_limit.either_pair_default
            limit.save()
        return limit

    def reset(self, user):
        base_limit = BaccaratLimit.objects.get_default()
        limit, _ = BaccaratUserLimit.objects.get_or_create(user=user)
        limit.player = base_limit.player_default
        limit.banker = base_limit.banker_default
        limit.tie = base_limit.tie_default
        limit.big = base_limit.big_default
        limit.small = base_limit.small_default
        limit.either_pair = base_limit.either_pair_default
        limit.save()
        return limit


class BaccaratUserLimit(models.Model):
    class Meta:
        ordering = ['-created_time']


    player = models.IntegerField(default=5)
    player_push = models.BooleanField(default=True)
    banker = models.IntegerField(default=5)
    banker_push = models.BooleanField(default=True)
    tie = models.IntegerField(default=5)
    tie_push = models.BooleanField(default=True)
    either_pair = models.IntegerField(default=5)
    either_pair_push = models.BooleanField(default=True)
    big = models.IntegerField(default=5)
    big_push = models.BooleanField(default=True)
    small = models.IntegerField(default=5)
    small_push = models.BooleanField(default=True)
    created_time = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, null=False)

    objects = BaccaratUserLimitManager()

    def json(self):
        return {
            "player": self.player,
            "player_push": self.player_push,
            "banker": self.banker,
            "banker_push": self.banker_push,
            "tie": self.tie,
            "tie_push": self.tie_push,
            "either_pair": self.either_pair,
            "either_pair_push": self.either_pair_push,
            "big": self.big,
            "big_push": self.big_push,
            "small": self.small,
            "small_push": self.small_push
        }


class PokerLimitManager(models.Manager):

    def get_default(self):
        try:
            limit = PokerLimit.objects.filter(active=True)[0]
        except:
            limit = PokerLimit.objects.create(active=True)
        return limit


class PokerLimit(models.Model):
    one_pair_min = models.IntegerField(default=1)
    one_pair_max = models.IntegerField(default=20)
    one_pair_default = models.IntegerField(default=15)
    one_pair_count_till = models.IntegerField(default=30)

    two_pairs_min = models.IntegerField(default=1)
    two_pairs_max = models.IntegerField(default=20)
    two_pairs_default = models.IntegerField(default=15)
    two_pairs_count_till = models.IntegerField(default=30)

    three_of_a_kind_min = models.IntegerField(default=1)
    three_of_a_kind_max = models.IntegerField(default=20)
    three_of_a_kind_default = models.IntegerField(default=15)
    three_of_a_kind_count_till = models.IntegerField(default=30)

    flush_min = models.IntegerField(default=1)
    flush_max = models.IntegerField(default=20)
    flush_default = models.IntegerField(default=15)
    flush_count_till = models.IntegerField(default=30)

    straight_min = models.IntegerField(default=1)
    straight_max = models.IntegerField(default=20)
    straight_default = models.IntegerField(default=15)
    straight_count_till = models.IntegerField(default=30)

    full_house_min = models.IntegerField(default=1)
    full_house_max = models.IntegerField(default=20)
    full_house_default = models.IntegerField(default=15)
    full_house_count_till = models.IntegerField(default=30)

    four_of_a_kind_min = models.IntegerField(default=1)
    four_of_a_kind_max = models.IntegerField(default=20)
    four_of_a_kind_default = models.IntegerField(default=15)
    four_of_a_kind_count_till = models.IntegerField(default=30)

    created_time = models.DateTimeField(auto_now_add=True)

    active = models.BooleanField(default=False)

    objects = PokerLimitManager()

    class Meta:
        ordering = ['active']


class PokerUserLimitManager(models.Manager):

    def get_default(self, user):
        try:
            limit = PokerUserLimit.objects.filter(user=user)[0]
        except:
            limit, _ = PokerUserLimit.objects.get_or_create(user=user)
            base_limit = PokerLimit.objects.get_default()
            limit.one_pair = base_limit.one_pair_default
            limit.two_pairs = base_limit.two_pairs_default
            limit.three_of_a_kind = base_limit.three_of_a_kind_default
            limit.flush = base_limit.flush_default
            limit.straight = base_limit.straight_default
            limit.full_house = base_limit.full_house_default
            limit.four_of_a_kind = base_limit.four_of_a_kind_default
            limit.save()
        return limit


    def reset(self, user):
        limit, _ = PokerUserLimit.objects.get_or_create(user=user)
        base_limit = PokerLimit.objects.get_default()
        limit.one_pair = base_limit.one_pair_default
        limit.two_pairs = base_limit.two_pairs_default
        limit.three_of_a_kind = base_limit.three_of_a_kind_default
        limit.flush = base_limit.flush_default
        limit.straight = base_limit.straight_default
        limit.full_house = base_limit.full_house_default
        limit.four_of_a_kind = base_limit.four_of_a_kind_default
        limit.save()
        return limit


class PokerUserLimit(models.Model):
    class Meta:
        ordering = ['-created_time']


    one_pair = models.IntegerField(default=5)
    one_pair_push = models.BooleanField(default=True)
    two_pairs = models.IntegerField(default=5)
    two_pairs_push = models.BooleanField(default=True)
    three_of_a_kind = models.IntegerField(default=5)
    three_of_a_kind_push = models.BooleanField(default=True)
    flush = models.IntegerField(default=5)
    flush_push = models.BooleanField(default=True)
    straight = models.IntegerField(default=5)
    straight_push = models.BooleanField(default=True)
    full_house = models.IntegerField(default=5)
    full_house_push = models.BooleanField(default=True)
    four_of_a_kind = models.IntegerField(default=5)
    four_of_a_kind_push = models.BooleanField(default=True)
    created_time = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, null=False)

    objects = PokerUserLimitManager()

    def json(self):
        return {
            "one_pair": self.one_pair,
            "one_pair_push": self.one_pair_push,
            "two_pairs": self.two_pairs,
            "two_pairs_push": self.two_pairs_push,
            "three_of_a_kind": self.three_of_a_kind,
            "three_of_a_kind_push": self.three_of_a_kind_push,
            "flush": self.flush,
            "flush_push": self.flush_push,
            "straight": self.straight,
            "straight_push": self.straight_push,
            "full_house": self.full_house,
            "full_house_push": self.full_house_push,
            "four_of_a_kind": self.four_of_a_kind,
            "four_of_a_kind_push": self.four_of_a_kind_push
        }


class Warbets(models.Model):
    uuid = models.CharField(max_length=15, unique=True, db_index=True)
    player = models.BooleanField(default=False, db_index=True)
    diller = models.BooleanField(default=False, db_index=True)
    draw = models.BooleanField(default=False, db_index=True)
    player_red = models.BooleanField(default=False, db_index=True)
    diller_red = models.BooleanField(default=False, db_index=True)
    player_black = models.BooleanField(default=False, db_index=True)
    diller_black = models.BooleanField(default=False, db_index=True)
    timestamp = models.DateTimeField(blank=False, null=False, db_index=True)
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']


class WarbetsLimitManager(models.Manager):

    def get_default(self):
        try:
            limit = WarbetsLimit.objects.filter(active=True)[0]
        except:
            limit = WarbetsLimit.objects.create(active=True)
        return limit


class WarbetsLimit(models.Model):
    player_min = models.IntegerField(default=1)
    player_max = models.IntegerField(default=20)
    player_default = models.IntegerField(default=15)
    player_count_till = models.IntegerField(default=30)

    diller_min = models.IntegerField(default=1)
    diller_max = models.IntegerField(default=20)
    diller_default = models.IntegerField(default=15)
    diller_count_till = models.IntegerField(default=30)

    draw_min = models.IntegerField(default=1)
    draw_max = models.IntegerField(default=20)
    draw_default = models.IntegerField(default=15)
    draw_count_till = models.IntegerField(default=30)

    player_red_min = models.IntegerField(default=1)
    player_red_max = models.IntegerField(default=20)
    player_red_default = models.IntegerField(default=15)
    player_red_count_till = models.IntegerField(default=30)

    diller_red_min = models.IntegerField(default=1)
    diller_red_max = models.IntegerField(default=20)
    diller_red_default = models.IntegerField(default=15)
    diller_red_count_till = models.IntegerField(default=30)

    player_black_min = models.IntegerField(default=1)
    player_black_max = models.IntegerField(default=20)
    player_black_default = models.IntegerField(default=15)
    player_black_count_till = models.IntegerField(default=30)

    diller_black_min = models.IntegerField(default=1)
    diller_black_max = models.IntegerField(default=20)
    diller_black_default = models.IntegerField(default=15)
    diller_black_count_till = models.IntegerField(default=30)

    just_black_min = models.IntegerField(default=1)
    just_black_max = models.IntegerField(default=20)
    just_black_default = models.IntegerField(default=15)
    just_black_count_till = models.IntegerField(default=30)

    just_red_min = models.IntegerField(default=1)
    just_red_max = models.IntegerField(default=20)
    just_red_default = models.IntegerField(default=15)
    just_red_count_till = models.IntegerField(default=30)

    created_time = models.DateTimeField(auto_now_add=True)

    active = models.BooleanField(default=False)

    objects = WarbetsLimitManager()

    class Meta:
        ordering = ['active']


class WarbetsUserLimitManager(models.Manager):

    def get_default(self, user):
        try:
            limit = WarbetsUserLimit.objects.filter(user=user)[0]
        except:
            limit, _ = WarbetsUserLimit.objects.get_or_create(user=user)
            base_limit = WarbetsLimit.objects.get_default()
            limit.player = base_limit.player_default
            limit.diller = base_limit.diller_default
            limit.draw = base_limit.draw_default
            limit.player_red = base_limit.player_red_default
            limit.diller_red = base_limit.diller_red_default
            limit.player_black = base_limit.player_black_default
            limit.diller_black = base_limit.diller_black_default
            limit.just_black = base_limit.just_black_default
            limit.just_red = base_limit.just_red_default
            limit.save()
        return limit

    def reset(self, user):
        limit, _ = WarbetsUserLimit.objects.get_or_create(user=user)
        base_limit = WarbetsLimit.objects.get_default()
        limit.player = base_limit.player_default
        limit.diller = base_limit.diller_default
        limit.draw = base_limit.draw_default
        limit.player_red = base_limit.player_red_default
        limit.diller_red = base_limit.diller_red_default
        limit.player_black = base_limit.player_black_default
        limit.diller_black = base_limit.diller_black_default
        limit.just_black = base_limit.just_black_default
        limit.just_red = base_limit.just_red_default
        limit.save()
        return limit


class WarbetsUserLimit(models.Model):
    class Meta:
        ordering = ['-created_time']


    player = models.IntegerField(default=10)
    player_push = models.BooleanField(default=True)
    diller = models.IntegerField(default=10)
    diller_push = models.BooleanField(default=True)
    draw = models.IntegerField(default=10)
    draw_push = models.BooleanField(default=True)
    player_red = models.IntegerField(default=10)
    player_red_push = models.BooleanField(default=True)
    diller_red = models.IntegerField(default=10)
    diller_red_push = models.BooleanField(default=True)
    player_black = models.IntegerField(default=10)
    player_black_push = models.BooleanField(default=True)
    diller_black = models.IntegerField(default=10)
    diller_black_push = models.BooleanField(default=True)

    just_black = models.IntegerField(default=10)
    just_black_push = models.BooleanField(default=True)

    just_red = models.IntegerField(default=10)
    just_red_push = models.BooleanField(default=True)

    created_time = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, null=False)

    objects = WarbetsUserLimitManager()

    def json(self):
        return {
            "player": self.player,
            "player_push": self.player_push,
            "diller": self.diller,
            "diller_push": self.diller_push,
            "draw": self.draw,
            "draw_push": self.draw_push,
            "player_red": self.player_red,
            "player_red_push": self.player_red_push,
            "diller_red": self.diller_red,
            "diller_red_push": self.diller_red_push,
            "player_black": self.player_black,
            "player_black_push": self.player_black_push,
            "diller_black": self.diller_black,
            "diller_black_push": self.diller_black_push,
            "just_black": self.just_black,
            "just_black_push": self.just_black_push,
            "just_red": self.just_red,
            "just_red_push": self.just_red_push
        }


class Wheel(models.Model):
    uuid = models.CharField(max_length=15, unique=True, db_index=True)
    d1_to_d6 = models.BooleanField(default=False, db_index=True)
    d7_to_d12 = models.BooleanField(default=False, db_index=True)
    d13_to_d18 = models.BooleanField(default=False, db_index=True)
    less = models.BooleanField(default=False, db_index=True)
    more = models.BooleanField(default=False, db_index=True)
    grey = models.BooleanField(default=False, db_index=True)
    red = models.BooleanField(default=False, db_index=True)
    black = models.BooleanField(default=False, db_index=True)
    even = models.BooleanField(default=False, db_index=True)
    odd = models.BooleanField(default=False, db_index=True)

    timestamp = models.DateTimeField(blank=False, null=False, db_index=True)
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']


class WheelLimitManager(models.Manager):

    def get_default(self):
        try:
            limit = WheelLimit.objects.filter(active=True)[0]
        except:
            limit = WheelLimit.objects.create(active=True)
        return limit


class WheelLimit(models.Model):
    d1_to_d6_min = models.IntegerField(default=1)
    d1_to_d6_max = models.IntegerField(default=20)
    d1_to_d6_default = models.IntegerField(default=15)
    d1_to_d6_count_till = models.IntegerField(default=30)

    d7_to_d12_min = models.IntegerField(default=1)
    d7_to_d12_max = models.IntegerField(default=20)
    d7_to_d12_default = models.IntegerField(default=15)
    d7_to_d12_count_till = models.IntegerField(default=30)

    d13_to_d18_min = models.IntegerField(default=1)
    d13_to_d18_max = models.IntegerField(default=20)
    d13_to_d18_default = models.IntegerField(default=15)
    d13_to_d18_count_till = models.IntegerField(default=30)

    less_min = models.IntegerField(default=1)
    less_max = models.IntegerField(default=20)
    less_default = models.IntegerField(default=15)
    less_count_till = models.IntegerField(default=30)

    more_min = models.IntegerField(default=1)
    more_max = models.IntegerField(default=20)
    more_default = models.IntegerField(default=15)
    more_count_till = models.IntegerField(default=30)

    grey_min = models.IntegerField(default=1)
    grey_max = models.IntegerField(default=20)
    grey_default = models.IntegerField(default=15)
    grey_count_till = models.IntegerField(default=30)

    black_min = models.IntegerField(default=1)
    black_max = models.IntegerField(default=20)
    black_default = models.IntegerField(default=15)
    black_count_till = models.IntegerField(default=30)

    red_min = models.IntegerField(default=1)
    red_max = models.IntegerField(default=20)
    red_default = models.IntegerField(default=15)
    red_count_till = models.IntegerField(default=30)

    even_min = models.IntegerField(default=1)
    even_max = models.IntegerField(default=20)
    even_default = models.IntegerField(default=15)
    even_count_till = models.IntegerField(default=30)

    odd_min = models.IntegerField(default=1)
    odd_max = models.IntegerField(default=20)
    odd_default = models.IntegerField(default=15)
    odd_count_till = models.IntegerField(default=30)

    created_time = models.DateTimeField(auto_now_add=True)

    active = models.BooleanField(default=False)

    objects = WheelLimitManager()

    class Meta:
        ordering = ['active']


class WheelUserLimitManager(models.Manager):

    def get_default(self, user):
        try:
            limit = WheelUserLimit.objects.filter(user=user)[0]
        except:
            limit, _ = WheelUserLimit.objects.get_or_create(user=user)
            base_limit = WheelLimit.objects.get_default()
            limit.d1_to_d6 = base_limit.d1_to_d6_default
            limit.d7_to_d12 = base_limit.d7_to_d12_default
            limit.d13_to_d18 = base_limit.d13_to_d18_default
            limit.less = base_limit.less_default
            limit.more = base_limit.more_default
            limit.grey = base_limit.grey_default
            limit.red = base_limit.red_default
            limit.black = base_limit.black_default
            limit.even = base_limit.even_default
            limit.odd = base_limit.odd_default
            limit.save()
        return limit

    def reset(self, user):
        limit, _ = WheelUserLimit.objects.get_or_create(user=user)
        base_limit = WheelLimit.objects.get_default()
        limit.d1_to_d6 = base_limit.d1_to_d6_default
        limit.d7_to_d12 = base_limit.d7_to_d12_default
        limit.d13_to_d18 = base_limit.d13_to_d18_default
        limit.less = base_limit.less_default
        limit.more = base_limit.more_default
        limit.grey = base_limit.grey_default
        limit.red = base_limit.red_default
        limit.black = base_limit.black_default
        limit.even = base_limit.even_default
        limit.odd = base_limit.odd_default
        limit.save()
        return limit


class WheelUserLimit(models.Model):
    class Meta:
        ordering = ['-created_time']

    d1_to_d6 = models.IntegerField(default=10)
    d1_to_d6_push = models.BooleanField(default=True, db_index=True)
    d7_to_d12 = models.IntegerField(default=10)
    d7_to_d12_push = models.BooleanField(default=True, db_index=True)
    d13_to_d18 = models.IntegerField(default=10)
    d13_to_d18_push = models.BooleanField(default=True, db_index=True)
    less = models.IntegerField(default=10)
    less_push = models.BooleanField(default=True, db_index=True)
    more = models.IntegerField(default=10)
    more_push = models.BooleanField(default=True, db_index=True)
    grey = models.IntegerField(default=10)
    grey_push = models.BooleanField(default=True, db_index=True)
    red = models.IntegerField(default=10)
    red_push = models.BooleanField(default=True, db_index=True)
    black = models.IntegerField(default=10)
    black_push = models.BooleanField(default=True, db_index=True)
    even = models.IntegerField(default=10)
    even_push = models.BooleanField(default=True, db_index=True)
    odd = models.IntegerField(default=10)
    odd_push = models.BooleanField(default=True, db_index=True)

    created_time = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, null=False)

    objects = WheelUserLimitManager()

    def json(self):
        return {
            "d1_to_d6": self.d1_to_d6,
            "d1_to_d6_push": self.d1_to_d6_push,
            "d7_to_d12": self.d7_to_d12,
            "d7_to_d12_push": self.d7_to_d12_push,
            "d13_to_d18": self.d13_to_d18,
            "d13_to_d18_push": self.d13_to_d18_push,
            "less": self.less,
            "less_push": self.less_push,
            "more": self.more,
            "more_push": self.more_push,
            "grey": self.grey,
            "grey_push": self.grey_push,
            "red": self.red,
            "red_push": self.red_push,
            "black": self.black,
            "black_push": self.black_push,
            "even": self.even,
            "even_push": self.even_push,
            "odd": self.odd,
            "odd_push": self.odd_push
        }


class DiceDuel(models.Model):
    uuid = models.CharField(max_length=15, unique=True, db_index=True)
    red = models.IntegerField(default=0)
    blue = models.IntegerField(default=0)
    red_win = models.BooleanField(default=False, db_index=True)
    blue_win = models.BooleanField(default=False, db_index=True)
    draw = models.BooleanField(default=False, db_index=True)

    timestamp = models.DateTimeField(blank=False, null=False, db_index=True)
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']


class DiceDuelLimitManager(models.Manager):

    def get_default(self):
        try:
            limit = DiceDuelLimit.objects.filter(active=True)[0]
        except:
            limit = DiceDuelLimit.objects.create(active=True)
        return limit


class DiceDuelLimit(models.Model):
    red_win_min = models.IntegerField(default=1)
    red_win_max = models.IntegerField(default=20)
    red_win_default = models.IntegerField(default=15)
    red_win_count_till = models.IntegerField(default=30)

    blue_win_min = models.IntegerField(default=1)
    blue_win_max = models.IntegerField(default=20)
    blue_win_default = models.IntegerField(default=15)
    blue_win_count_till = models.IntegerField(default=30)

    draw_min = models.IntegerField(default=1)
    draw_max = models.IntegerField(default=20)
    draw_default = models.IntegerField(default=15)
    draw_count_till = models.IntegerField(default=30)

    created_time = models.DateTimeField(auto_now_add=True)

    active = models.BooleanField(default=False)

    objects = DiceDuelLimitManager()

    class Meta:
        ordering = ['active']


class DiceDuelUserLimitManager(models.Manager):

    def get_default(self, user):
        try:
            limit = DiceDuelUserLimit.objects.filter(user=user)[0]
        except:
            limit, _ = DiceDuelUserLimit.objects.get_or_create(user=user)
            base_limit = DiceDuelLimit.objects.get_default()
            limit.red_win = base_limit.red_win_default
            limit.blue_win = base_limit.blue_win_default
            limit.draw = base_limit.draw_default
            limit.save()
        return limit

    def reset(self, user):
        limit, _ = DiceDuelUserLimit.objects.get_or_create(user=user)
        base_limit = DiceDuelLimit.objects.get_default()
        limit.red_win = base_limit.red_win_default
        limit.blue_win = base_limit.blue_win_default
        limit.draw = base_limit.draw_default
        limit.save()
        return limit


class DiceDuelUserLimit(models.Model):
    class Meta:
        ordering = ['-created_time']


    blue_win = models.IntegerField(default=10)
    blue_win_push = models.BooleanField(default=True, db_index=True)

    red_win = models.IntegerField(default=10)
    red_win_push = models.BooleanField(default=True, db_index=True)

    draw = models.IntegerField(default=10)
    draw_push = models.BooleanField(default=True, db_index=True)

    created_time = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, null=False)

    objects = DiceDuelUserLimitManager()

    def json(self):
        return {
            "blue_win": self.blue_win,
            "blue_win_push": self.blue_win_push,
            "red_win": self.red_win,
            "red_win_push": self.red_win_push,
            "draw": self.draw,
            "draw_push": self.draw_push
        }


class Cache(models.Model):
    """
    Stores information about activations
    """
    name = models.CharField(max_length=2555, blank=False, db_index=True, unique=True)
    value = models.TextField(max_length=15000, blank=True)
    new = models.BooleanField(default=True, db_index=True)
    timestamp = models.DateTimeField(auto_now_add=True)
