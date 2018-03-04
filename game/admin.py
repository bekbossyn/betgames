from django.contrib import admin

from game.models import Baccarat, BaccaratLimit, BaccaratUserLimit, Poker, PokerLimit, PokerUserLimit, Warbets, Wheel, \
    WarbetsLimit, WheelLimit, DiceDuel, DiceDuelLimit, DiceDuelUserLimit, WheelUserLimit, WarbetsUserLimit


@admin.register(Baccarat)
class BaccaratAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'tie', 'banker', 'player', 'small', 'big', 'either_pair', 'timestamp')


@admin.register(Poker)
class PokerAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'one_pair', 'two_pairs', 'flush', 'straight', 'three_of_a_kind', 'full_house', 'four_of_a_kind', 'hand', 'timestamp')


@admin.register(BaccaratLimit)
class BaccaratLimitAdmin(admin.ModelAdmin):
    list_display = ['player_min',
                    'player_max',
                    'banker_min',
                    'banker_max',
                    'tie_min',
                    'tie_max',
                    'either_pair_min',
                    'either_pair_max',
                    'big_min',
                    'big_max',
                    'small_min',
                    'small_max',
                    'active']

    list_filter = ('active',)


@admin.register(BaccaratUserLimit)
class BaccaratUserLimitAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_time')


@admin.register(PokerLimit)
class PokerLimitAdmin(admin.ModelAdmin):
    list_display = ["one_pair_min",
                    "one_pair_max",
                    "one_pair_default",
                    "one_pair_count_till",
                    "two_pairs_min",
                    "two_pairs_max",
                    "two_pairs_default",
                    "two_pairs_count_till",
                    "three_of_a_kind_min",
                    "three_of_a_kind_max",
                    "three_of_a_kind_default",
                    "three_of_a_kind_count_till",
                    "flush_min",
                    "flush_max",
                    "flush_default",
                    "flush_count_till",
                    "straight_min",
                    "straight_max",
                    "straight_default",
                    "straight_count_till",
                    "full_house_min",
                    "full_house_max",
                    "full_house_default",
                    "full_house_count_till",
                    "four_of_a_kind_min",
                    "four_of_a_kind_max",
                    "four_of_a_kind_default",
                    "four_of_a_kind_count_till",
                    "active"]

    list_filter = ('active',)


@admin.register(PokerUserLimit)
class PokerUserLimitAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_time')


@admin.register(Warbets)
class WarbetsAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'player', 'diller', 'draw', 'player_red', 'player_black', 'diller_red', 'diller_black', 'timestamp')


@admin.register(WarbetsLimit)
class WarbetsLimitAdmin(admin.ModelAdmin):
    pass


@admin.register(WarbetsUserLimit)
class WarbetsUserLimitAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_time')


@admin.register(Wheel)
class WheelAdmin(admin.ModelAdmin):
    list_display = ("uuid", "d1_to_d6","d7_to_d12","d13_to_d18","less","more","grey","red","black","even","odd", "timestamp")


@admin.register(WheelLimit)
class WheelLimitAdmin(admin.ModelAdmin):
    pass


@admin.register(WheelUserLimit)
class WheelUserLimitAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_time')


@admin.register(DiceDuel)
class DiceDuelAdmin(admin.ModelAdmin):
    list_display = ('red', 'blue', 'red_win', 'blue_win', 'draw', 'timestamp')


@admin.register(DiceDuelLimit)
class DiceDuelLimitAdmin(admin.ModelAdmin):
    pass


@admin.register(DiceDuelUserLimit)
class DiceDuelUserLimitAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_time')
