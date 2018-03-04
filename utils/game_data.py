import json

from game.models import WheelLimit, WarbetsLimit, Warbets, Wheel, Poker, PokerLimit, Baccarat, BaccaratLimit, \
    DiceDuelLimit, DiceDuel, Cache


def _warbets_data():
    try:
        data = Cache.objects.filter(name='warbets', new=False)[0]
        return json.loads(data.value)
    except:
        pass
    limit = WarbetsLimit.objects.get_default()
    result = {
        "player": 0,
        "diller": 0,
        "draw": 0,
        "player_red": 0,
        "player_black": 0,
        "diller_red": 0,
        "diller_black": 0,
        "just_black": 0,
        "just_red": 0
    }
    for p in ["player", "diller", "draw", "player_red", "player_black", "diller_red", "diller_black"]:
        for i, b in enumerate(Warbets.objects.all()[:getattr(limit, "{}_count_till".format(p), 100)]):
            if getattr(b, p, False):
                break
            result[p] += 1
    for b in Warbets.objects.all()[:limit.just_black_count_till]:
        if not b.diller_black:
            result['just_black'] += 1
        else:
            break
        if not b.player_black:
            result['just_black'] += 1
        else:
            break
    for b in Warbets.objects.all()[:limit.just_red_count_till]:
        if not b.diller_red:
            result['just_red'] += 1
        else:
            break
        if not b.player_red:
            result['just_red'] += 1
        else:
            break
    return result


def _wheel_data():
    try:
        data = Cache.objects.filter(name='wheel', new=False)[0]
        return json.loads(data.value)
    except:
        pass
    limit = WheelLimit.objects.get_default()
    result = {
        "d1_to_d6": 0,
        "d7_to_d12": 0,
        "d13_to_d18": 0,
        "less": 0,
        "more": 0,
        "grey": 0,
        "red": 0,
        "black": 0,
        "even": 0,
        "odd": 0
    }

    for p in ["d1_to_d6","d7_to_d12","d13_to_d18","less","more","grey","red","black","even","odd"]:
        for i, b in enumerate(Wheel.objects.all()[:getattr(limit, "{}_count_till".format(p), 100)]):
            if getattr(b, p, False):
                break
            result[p] += 1
    return result


def _poker_data():
    try:
        data = Cache.objects.filter(name='poker', new=False)[0]
        return json.loads(data.value)
    except:
        pass
    limit = PokerLimit.objects.get_default()
    one_pair = 0
    two_pairs = 0
    three_of_a_kind = 0
    flush = 0
    straight = 0
    full_house = 0
    four_of_a_kind = 0
    for i, b in enumerate(Poker.objects.all()[:limit.one_pair_count_till]):
        if b.one_pair:
            break
        one_pair += 1
    for i, b in enumerate(Poker.objects.all()[:limit.two_pairs_count_till]):
        if b.two_pairs:
            break
        two_pairs += 1
    for i, b in enumerate(Poker.objects.all()[:limit.three_of_a_kind_count_till]):
        if b.three_of_a_kind:
            break
        three_of_a_kind += 1
    for i, b in enumerate(Poker.objects.all()[:limit.flush_count_till]):
        if b.flush:
            break
        flush += 1
    for i, b in enumerate(Poker.objects.all()[:limit.straight_count_till]):
        if b.straight:
            break
        straight += 1
    for i, b in enumerate(Poker.objects.all()[:limit.full_house_count_till]):
        if b.full_house:
            break
        full_house += 1
    for i, b in enumerate(Poker.objects.all()[:limit.four_of_a_kind_count_till]):
        if b.four_of_a_kind:
            break
        four_of_a_kind += 1

    return {
        "one_pair": one_pair,
        "two_pairs": two_pairs,
        "three_of_a_kind": three_of_a_kind,
        "flush": flush,
        "straight": straight,
        "full_house": full_house,
        "four_of_a_kind": four_of_a_kind
    }


def _baccart_data():
    try:
        data = Cache.objects.filter(name='baccarat', new=False)[0]
        return json.loads(data.value)
    except:
        pass

    limit = BaccaratLimit.objects.get_default()
    player = 0
    banker = 0
    tie = 0
    either_pair = 0
    small = 0
    big = 0

    for i, b in enumerate(Baccarat.objects.all()[:limit.player_count_till]):
        if b.player:
            break
        player += 1

    for i, b in enumerate(Baccarat.objects.all()[:limit.banker_count_till]):
        if b.banker:
            break
        banker += 1

    for i, b in enumerate(Baccarat.objects.all()[:limit.tie_count_till]):
        if b.tie:
            break
        tie += 1

    for i, b in enumerate(Baccarat.objects.all()[:limit.either_pair_count_till]):
        if b.either_pair:
            break
        either_pair += 1

    for i, b in enumerate(Baccarat.objects.all()[:limit.small_count_till]):
        if b.small:
            break
        small += 1

    for i, b in enumerate(Baccarat.objects.all()[:limit.big_count_till]):
        if b.big:
            break
        big += 1
    return {
        "player": player,
        "banker": banker,
        "tie": tie,
        "either_pair": either_pair,
        "small": small,
        "big": big
    }


def _dice_duel_data():
    try:
        data = Cache.objects.filter(name='dice_duel', new=False)[0]
        return json.loads(data.value)
    except:
        pass
    limit = DiceDuelLimit.objects.get_default()
    result = {
        "red_win": 0,
        "blue_win": 0,
        "draw": 0
    }

    for p in ["red_win","blue_win","draw"]:
        for i, b in enumerate(DiceDuel.objects.all()[:getattr(limit, "{}_count_till".format(p), 100)]):
            if getattr(b, p, False):
                break
            result[p] += 1
    return result
