# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt

from game.models import Baccarat, BaccaratLimit, BaccaratUserLimit, PokerUserLimit, PokerLimit, Poker, WarbetsLimit, \
    Warbets, WarbetsUserLimit, Wheel, WheelLimit, WheelUserLimit, DiceDuelUserLimit, DiceDuel, DiceDuelLimit
from main.models import Feedback
from main.tasks import email
from utils import http, codes, onesignal
from utils.game_data import _baccart_data, _poker_data, _warbets_data, _wheel_data, _dice_duel_data
from utils.parser import BACCARAT_NAMES, POKER_NAMES, WARBETS_NAMES, WHEEL_NAMES, DICE_DUEL_NAMES

User = get_user_model()


@http.json_response()
@http.requires_token()
@csrf_exempt
def info(request, user):
    if user.days_left() == 0:
        return {
            "code": 0,
            "games": [],
            "message": u"Закончился тариф",
            "user": user.json()
        }

    games = list()

    current_data = _baccart_data()
    user_data = BaccaratUserLimit.objects.get_default(user).json()
    baccarat_games = list()
    for p in ["player", "banker", "tie", "either_pair", "big", "small"]:
        baccarat_games.append({
            "name": BACCARAT_NAMES[p],
            "current_data": current_data[p],
            "user_data": user_data[p],
            "user_push": user_data["{}_push".format(p)],
            "param_name": "baccarat_{}".format(p)
        })

    try:
        last_poker_game = Poker.objects.all()[0].uuid
    except:
        last_poker_game = u'000000000000'

    try:
        last_baccarat_game = Baccarat.objects.all()[0].uuid
    except:
        last_baccarat_game = u'000000000000'

    try:
        last_warbets_game = Warbets.objects.all()[0].uuid
    except:
        last_warbets_game = u'000000000000'

    try:
        last_wheel_game = Wheel.objects.all()[0].uuid
    except:
        last_wheel_game = u'000000000000'


    try:
        last_dice_duel_game = DiceDuel.objects.all()[0].uuid
    except:
        last_dice_duel_game = u'000000000000'

    games.append({
        "name": u"Баккара",
        "data": baccarat_games,
        "last_game": last_baccarat_game
    })

    current_data = _poker_data()
    user_data = PokerUserLimit.objects.get_default(user).json()
    poker_games = list()
    for p in ["one_pair", "two_pairs", "three_of_a_kind",  "straight", "flush", "full_house", "four_of_a_kind"]:
        poker_games.append({
            "name": POKER_NAMES[p],
            "current_data": current_data[p],
            "user_data": user_data[p],
            "user_push": user_data["{}_push".format(p)],
            "param_name": "poker_{}".format(p)
        })

    games.append({
        "name": u"Покер",
        "data": poker_games,
        "last_game": last_poker_game
    })


    # ------------Warbets------------------

    current_data = _warbets_data()
    user_data = WarbetsUserLimit.objects.get_default(user).json()
    warbets_games = list()
    for p in ["player", "diller", "draw", "player_red", "player_black", "diller_red", "diller_black", "just_black", "just_red"]:
        warbets_games.append({
            "name": WARBETS_NAMES[p],
            "current_data": current_data[p],
            "user_data": user_data[p],
            "user_push": user_data["{}_push".format(p)],
            "param_name": "warbets_{}".format(p)
        })
    games.append({
        "name": u"Битва ставок",
        "data": warbets_games,
        "last_game": last_warbets_game
    })

    # ------------END-Warbets------------------

    # ------------Wheel------------------

    current_data = _wheel_data()
    user_data = WheelUserLimit.objects.get_default(user).json()
    wheel_games = list()
    for p in ["d1_to_d6","d7_to_d12","d13_to_d18","less","more","grey","red","black","even","odd"]:
        wheel_games.append({
            "name": WHEEL_NAMES[p],
            "current_data": current_data[p],
            "user_data": user_data[p],
            "user_push": user_data["{}_push".format(p)],
            "param_name": "wheel_{}".format(p)
        })
    games.append({
        "name": u"Колесо",
        "data": wheel_games,
        "last_game": last_wheel_game
    })

    # ------------END-Wheel------------------

    # ------------DICE-DUEL------------------

    current_data = _dice_duel_data()
    user_data = DiceDuelUserLimit.objects.get_default(user).json()
    dice_duel_games = list()
    for p in ["red_win", "blue_win", "draw"]:
        dice_duel_games.append({
            "name": DICE_DUEL_NAMES[p],
            "current_data": current_data[p],
            "user_data": user_data[p],
            "user_push": user_data["{}_push".format(p)],
            "param_name": "dice_duel_{}".format(p)
        })
    games.append({
        "name": u"Дуэль костей",
        "data": dice_duel_games,
        "last_game": last_dice_duel_game
    })

    # ------------END-DICE-DUEL--------------

    return {
        "user": user.json(),
        "games": games
    }


@http.json_response()
@http.required_methods("POST")
@http.requires_token()
@http.required_parameters(["param_names", "value"])
@csrf_exempt
def update_push(request, user):
    for param_name in request.POST.getlist('param_names'):
        if param_name.startswith('baccarat'):
            game_type = param_name[len('baccarat') + 1:] + "_push"
            user_limit = BaccaratUserLimit.objects.get_default(user)
            setattr(user_limit, game_type, request.POST["value"].lower() == "true")
            user_limit.save()
        if param_name.startswith('poker'):
            game_type = param_name[len('poker') + 1:] + "_push"
            user_limit = PokerUserLimit.objects.get_default(user)
            setattr(user_limit, game_type, request.POST["value"].lower() == "true")
            user_limit.save()
        if param_name.startswith('wheel'):
            game_type = param_name[len('wheel') + 1:] + "_push"
            user_limit = WheelUserLimit.objects.get_default(user)
            setattr(user_limit, game_type, request.POST["value"].lower() == "true")
            user_limit.save()
        if param_name.startswith('warbets'):
            game_type = param_name[len('warbets') + 1:] + "_push"
            user_limit = WarbetsUserLimit.objects.get_default(user)
            setattr(user_limit, game_type, request.POST["value"].lower() == "true")
            user_limit.save()
        if param_name.startswith('dice_duel'):
            game_type = param_name[len('dice_duel') + 1:] + "_push"
            user_limit = DiceDuelUserLimit.objects.get_default(user)
            setattr(user_limit, game_type, request.POST["value"].lower() == "true")
            user_limit.save()
    return http.ok_response()


@http.json_response()
@http.requires_token()
@http.required_parameters(["push_token"])
@csrf_exempt
def update_token(request, user):
    if User.objects.filter(push_token=request.POST["push_token"]).exclude(pk=user.pk).exists():
        other = User.objects.filter(push_token=request.POST["push_token"]).exclude(pk=user.pk)[0]
        try:
            email.delay(settings.ADMINS_LIST,
                    u"ВНИМАНИЕ! Дублирующий push #{}".format(user.phone),
                    u"ВНИМАНИЕ! Дублирующий push у {} с {}".format(user.phone, other.phone))
        except:
            pass
    User.objects.filter(push_token=request.POST["push_token"]).update(push_token="")
    user.push_token = request.POST["push_token"]
    user.save()
    return http.ok_response()


@http.json_response()
@http.requires_token()
@http.required_parameters(["value"])
@csrf_exempt
def update_sound(request, user):
    user.sound = request.POST["value"].lower() == "true"
    user.save()
    return {
        "user": user.json()
    }


@http.json_response()
@http.requires_token()
@csrf_exempt
def test_push(request, user):
    onesignal.to_users(user.push_token, user.sound, user.sound_name, u"Тестовое уведомление", u"Тестовое уведомление", u"Тестовое уведомление", 'test', 50, {"is_test": True})
    user.save()
    return {
        "user": user.json()
    }


@http.json_response()
@http.requires_token()
@http.required_parameters(["sound_name"])
@csrf_exempt
def update_sound_name(request, user):
    user.sound_name = request.POST["sound_name"]
    user.save()
    return {
        "user": user.json()
    }


@http.json_response()
@http.requires_token()
@http.required_parameters(["message"])
@csrf_exempt
def send_feedback(request, user):
    Feedback.objects.create(message=request.POST["message"], user=user)
    email.delay(settings.ADMINS_LIST, u'Запрос в службу поддержки {}'.format(user.phone), request.POST["message"])
    return http.ok_response()


@http.json_response()
@http.requires_token()
@csrf_exempt
def reset(request, user):
    BaccaratUserLimit.objects.reset(user)
    PokerUserLimit.objects.reset(user)
    WarbetsUserLimit.objects.reset(user)
    WheelUserLimit.objects.reset(user)
    return http.ok_response()


@http.json_response()
@http.requires_token()
@http.required_parameters(["param_name", "param_val"])
@csrf_exempt
def update(request, user):
    param_name = request.POST["param_name"]

    if param_name.startswith('baccarat'):
        game_type = param_name[len('baccarat') + 1:]
        baccarat_limit = BaccaratLimit.objects.get_default()
        user_limit = BaccaratUserLimit.objects.get_default(user)
        if getattr(baccarat_limit, game_type + "_min") > int(request.POST["param_val"]):
            return {
                "code": codes.BAD_REQUEST,
                "param_val": getattr(user_limit, game_type),
                "message": u"Минимальное кол-во {}".format(getattr(baccarat_limit, game_type + "_min"))
            }

        if getattr(baccarat_limit, game_type + "_max") < int(request.POST["param_val"]):
            return {
                "code": codes.BAD_REQUEST,
                "param_val": getattr(user_limit, game_type),
                "message": u"Максимальное кол-во {}".format(getattr(baccarat_limit, game_type + "_max"))
            }

        setattr(user_limit, game_type, int(request.POST["param_val"]))

        user_limit.save()

        return {
            "code": codes.OK,
            "value": getattr(user_limit, game_type)
        }

    if param_name.startswith('poker'):
        game_type = param_name[len('poker') + 1:]
        poker_limit = PokerLimit.objects.get_default()
        user_limit = PokerUserLimit.objects.get_default(user)
        if getattr(poker_limit, game_type + "_min") > int(request.POST["param_val"]):
            return {
                "code": codes.BAD_REQUEST,
                "param_val": getattr(user_limit, game_type),
                "message": u"Минимальное кол-во {}".format(getattr(poker_limit, game_type + "_min"))
            }

        if getattr(poker_limit, game_type + "_max") < int(request.POST["param_val"]):
            return {
                "code": codes.BAD_REQUEST,
                "param_val": getattr(user_limit, game_type),
                "message": u"Максимальное кол-во {}".format(getattr(poker_limit, game_type + "_max"))
            }

        setattr(user_limit, game_type, int(request.POST["param_val"]))

        user_limit.save()

        return {
            "code": codes.OK,
            "param_val": getattr(user_limit, game_type)
        }

    if param_name.startswith('wheel'):
        game_type = param_name[len('wheel') + 1:]
        wheel_limit = WheelLimit.objects.get_default()
        user_limit = WheelUserLimit.objects.get_default(user)
        if getattr(wheel_limit, game_type + "_min") > int(request.POST["param_val"]):
            return {
                "code": codes.BAD_REQUEST,
                "param_val": getattr(user_limit, game_type),
                "message": u"Минимальное кол-во {}".format(getattr(wheel_limit, game_type + "_min"))
            }

        if getattr(wheel_limit, game_type + "_max") < int(request.POST["param_val"]):
            return {
                "code": codes.BAD_REQUEST,
                "param_val": getattr(user_limit, game_type),
                "message": u"Максимальное кол-во {}".format(getattr(wheel_limit, game_type + "_max"))
            }

        setattr(user_limit, game_type, int(request.POST["param_val"]))

        user_limit.save()

        return {
            "code": codes.OK,
            "param_val": getattr(user_limit, game_type)
        }

    if param_name.startswith('warbets'):
        game_type = param_name[len('warbets') + 1:]
        warbets_limit = WarbetsLimit.objects.get_default()
        user_limit = WarbetsUserLimit.objects.get_default(user)
        if getattr(warbets_limit, game_type + "_min") > int(request.POST["param_val"]):
            return {
                "code": codes.BAD_REQUEST,
                "param_val": getattr(user_limit, game_type),
                "message": u"Минимальное кол-во {}".format(getattr(warbets_limit, game_type + "_min"))
            }

        if getattr(warbets_limit, game_type + "_max") < int(request.POST["param_val"]):
            return {
                "code": codes.BAD_REQUEST,
                "param_val": getattr(user_limit, game_type),
                "message": u"Максимальное кол-во {}".format(getattr(warbets_limit, game_type + "_max"))
            }

        setattr(user_limit, game_type, int(request.POST["param_val"]))

        user_limit.save()

        return {
            "code": codes.OK,
            "param_val": getattr(user_limit, game_type)
        }
    if param_name.startswith('dice_duel'):
        game_type = param_name[len('dice_duel') + 1:]
        dice_duel_limit = DiceDuelLimit.objects.get_default()
        user_limit = DiceDuelUserLimit.objects.get_default(user)
        if getattr(dice_duel_limit, game_type + "_min") > int(request.POST["param_val"]):
            return {
                "code": codes.BAD_REQUEST,
                "param_val": getattr(user_limit, game_type),
                "message": u"Минимальное кол-во {}".format(getattr(dice_duel_limit, game_type + "_min"))
            }

        if getattr(dice_duel_limit, game_type + "_max") < int(request.POST["param_val"]):
            return {
                "code": codes.BAD_REQUEST,
                "param_val": getattr(user_limit, game_type),
                "message": u"Максимальное кол-во {}".format(getattr(dice_duel_limit, game_type + "_max"))
            }

        setattr(user_limit, game_type, int(request.POST["param_val"]))

        user_limit.save()

        return {
            "code": codes.OK,
            "param_val": getattr(user_limit, game_type)
        }
    return {
        "code": codes.BAD_REQUEST,
        "message": u"Параметр не найден"
    }
