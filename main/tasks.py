# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from datetime import datetime, timedelta
from django.core.mail import send_mail, EmailMessage

from celery import shared_task
from django.conf import settings

from game.models import Baccarat, Poker, Warbets, Wheel, WheelUserLimit, WarbetsUserLimit, PokerUserLimit, \
    BaccaratUserLimit, DiceDuel, DiceDuelUserLimit, Cache

from utils import parser, onesignal
from utils.game_data import _wheel_data, _warbets_data, _poker_data, _baccart_data, _dice_duel_data


def its_time(a, b, delay_in_seconds):
    if a.day != b.day or a.month != b.month or a.year != b.year:
        return True
    a0 = a.replace(hour=1, minute=1, second=1, month=1, year=a.year - 1)
    b0 = b.replace(hour=1, minute=1, second=1, month=1, year=b.year - 1)
    t1 = (b - b0).total_seconds()
    t2 = (a - a0).total_seconds()
    return t2 - t1 >= delay_in_seconds


@shared_task
def email(to, subject, message):
    try:
        to[0]
    except:
        to = [to]
    send_mail(subject=subject,
              from_email=settings.FROM_EMAIL,
              recipient_list=to,
              message=message)


@shared_task
def baccarat():
    """
    Celery task for parsing results of Baccarat game.
    Timezone is UTC
    :return:
    """
    utcnow = datetime.utcnow()
    if Baccarat.objects.all().count() == 0 or its_time(utcnow, Baccarat.objects.all()[0].timestamp, 60):
        results = parser.get_baccarat(utcnow.year, utcnow.month, utcnow.day)
        new_uuids = list()
        for r in results:
            if Baccarat.objects.filter(uuid=r['id']).exists():
                b = Baccarat.objects.get(uuid=r['id'])
            else:
                created_time = utcnow.replace(hour=int(r['timestamp'][:2]),
                                              minute=int(r['timestamp'][3:5]),
                                              second=int(r['timestamp'][6:8]))
                b = Baccarat.objects.create(uuid=r['id'], raw_result=','.join(r['result']), timestamp=created_time)
                b.tie = "Tie" in r['result']
                new_uuids.append(b.uuid)
            b.banker = "Banker" in r['result']
            b.player = "Player" in r['result']
            b.small = "Small" in r['result']
            b.big = "Big" in r['result']
            b.either_pair = "Either pair" in r['result']
            b.save()

        for b in Baccarat.objects.all()[15000:]:
            b.delete()

        if len(new_uuids) > 0:
            c, _ = Cache.objects.get_or_create(name='baccarat')
            c.new = True
            c.save()
            data = _baccart_data()
            for w in BaccaratUserLimit.objects.all():
                if w.user.push_token and w.user.days_left() > 0:
                    for k, v in data.items():
                        if getattr(w, "{}_push".format(k)) and v >= getattr(w, k):
                            onesignal.to_users(w.user.push_token, w.user.sound, w.user.sound_name, u"Баккара", u"Баккара: {}".format(parser.BACCARAT_NAMES[k].lower()), u"Количество ходов уже: {}".format(v), k, 30)
        return len(new_uuids)

    return []


@shared_task
def poker():
    """
    Celery task for parsing results of Baccarat game.
    Timezone is UTC
    :return:
    """
    utcnow = datetime.utcnow()
    if Poker.objects.all().count() == 0 or its_time(utcnow, Poker.objects.all()[0].timestamp, 4 * 60):
        results = parser.get_poker(utcnow.year, utcnow.month, utcnow.day)
        new_uuids = list()
        for r in results:
            if not Poker.objects.filter(uuid=r['id']).exists():
                created_time = utcnow.replace(hour=int(r['timestamp'][:2]),
                                              minute=int(r['timestamp'][3:5]),
                                              second=int(r['timestamp'][6:8]))
                b = Poker.objects.create(uuid=r['id'], hand=r['hand'], timestamp=created_time)
                new_uuids.append(b.uuid)
                b.one_pair = "one pair" in r['result']
                b.two_pairs = "two pairs" in r['result']
                b.three_of_a_kind = "three of a kind" in r['result']
                b.flush = "flush" in r['result']
                b.straight = "straight" in r['result']
                b.full_house = "full house" in r['result']
                b.four_of_a_kind = "four of a kind" in r['result']
                b.save()

        for b in Poker.objects.all()[15000:]:
            b.delete()

        if len(new_uuids) > 0:
            c, _ = Cache.objects.get_or_create(name='poker')
            c.new = True
            c.save()
            data = _poker_data()
            for w in PokerUserLimit.objects.all():
                if w.user.push_token and w.user.days_left() > 0:
                    for k, v in data.items():
                        if getattr(w, "{}_push".format(k)) and v >= getattr(w, k):
                            onesignal.to_users(w.user.push_token, w.user.sound, w.user.sound_name, u"Покер", u"Покер: {}".format(parser.POKER_NAMES[k].lower()), u"Количество ходов уже: {}".format(v), k, 30)
        return len(new_uuids)
    return 0


@shared_task
def warbets():
    """
    Celery task for parsing results of War of Bets game.
    Timezone is UTC
    :return:
    """
    utcnow = datetime.utcnow()
    if Warbets.objects.all().count() == 0 or its_time(utcnow, Warbets.objects.all()[0].timestamp, 45):
        results = parser.get_warbets(utcnow.year, utcnow.month, utcnow.day)
        new_uuids = list()
        for r in results:
            if not Warbets.objects.filter(uuid=r['id']).exists():
                created_time = utcnow.replace(hour=int(r['timestamp'][:2]),
                                              minute=int(r['timestamp'][3:5]),
                                              second=int(r['timestamp'][6:8]))
                b = Warbets.objects.create(uuid=r['id'], timestamp=created_time)
                new_uuids.append(b.uuid)
                b.player = r['player_win']
                b.diller = r['diller_win']
                b.player_red = r['player_red']
                b.player_black = not r['player_red']
                b.diller_red = r['diller_red']
                b.diller_black = not r['diller_red']
                b.draw = not r['player_win'] and not r['diller_win']
                b.save()

        for b in Warbets.objects.all()[15000:]:
            b.delete()

        if len(new_uuids) > 0:
            c, _ = Cache.objects.get_or_create(name='warbets')
            c.new = True
            c.save()
            data = _warbets_data()
            for w in WarbetsUserLimit.objects.all():
                if w.user.push_token and w.user.days_left() > 0:
                    for k, v in data.items():
                        if getattr(w, "{}_push".format(k)) and v >= getattr(w, k):
                            onesignal.to_users(w.user.push_token, w.user.sound, w.user.sound_name, u"Битва ставок", u"Битва ставок: {}".format(parser.WARBETS_NAMES[k].lower()), u"Количество ходов уже: {}".format(v), k, 30)
        return len(new_uuids)
    return 0


@shared_task
def wheel():
    """
    Celery task for parsing results of War of Bets game.
    Timezone is UTC
    :return:
    """
    utcnow = datetime.utcnow()

    if Wheel.objects.all().count() == 0 or its_time(utcnow, Wheel.objects.all()[0].timestamp, 2 * 60 + 45):
        results = parser.get_wheel(utcnow.year, utcnow.month, utcnow.day)
        new_uuids = list()
        for r in results:
            if not Wheel.objects.filter(uuid=r['id']).exists():
                created_time = utcnow.replace(hour=int(r['timestamp'][:2]),
                                              minute=int(r['timestamp'][3:5]),
                                              second=int(r['timestamp'][6:8]))
                b = Wheel.objects.create(uuid=r['id'], timestamp=created_time)
                new_uuids.append(b.uuid)
                b.d1_to_d6 = 1 <= r['number'] <= 6
                b.d7_to_d12 = 7 <= r['number'] <= 12
                b.d13_to_d18 = 13 <= r['number'] <= 18
                b.less = r['number'] < 10
                b.more = r['number'] > 9
                b.grey = "grey" in r['color'].lower()
                b.red = "red" in r['color'].lower()
                b.black = "black" in r['color'].lower()
                b.even = r['number'] % 2 == 0
                b.odd = r['number'] % 2 != 0
                b.save()

        for b in Wheel.objects.all()[15000:]:
            b.delete()
        if len(new_uuids) > 0:
            c, _ = Cache.objects.get_or_create(name='wheel')
            c.new = True
            c.save()
            data = _wheel_data()
            for w in WheelUserLimit.objects.all():
                if w.user.push_token and w.user.days_left() > 0:
                    for k, v in data.items():
                        if getattr(w, "{}_push".format(k)) and v >= getattr(w, k):
                            onesignal.to_users(w.user.push_token, w.user.sound, w.user.sound_name, u"Колесо", u"Колесо: {}".format(parser.WHEEL_NAMES[k].lower()), u"Количество ходов уже: {}".format(v), k, 30)
        return len(new_uuids)
    return 0


@shared_task
def dice_duel():
    """
    Celery task for parsing results of War of Bets game.
    Timezone is UTC
    :return:
    """
    utcnow = datetime.utcnow()
    if DiceDuel.objects.all().count() == 0 or its_time(utcnow, DiceDuel.objects.all()[0].timestamp, 2 * 60 + 45):
        results = parser.get_dice_duel(utcnow.year, utcnow.month, utcnow.day)
        new_uuids = list()
        for r in results:
            if not DiceDuel.objects.filter(uuid=r['id']).exists():
                created_time = utcnow.replace(hour=int(r['timestamp'][:2]),
                                              minute=int(r['timestamp'][3:5]),
                                              second=int(r['timestamp'][6:8]))
                b = DiceDuel.objects.create(uuid=r['id'], timestamp=created_time)
                new_uuids.append(b.uuid)
                b.red = r['red']
                b.blue = r['blue']
                b.blue_win = r['blue'] > r['red']
                b.red_win = r['red'] > r['blue']
                b.draw = r['red'] == r['blue']
                b.save()

        for b in DiceDuel.objects.all()[15000:]:
            b.delete()
        if len(new_uuids) > 0:
            c, _ = Cache.objects.get_or_create(name='dice_duel')
            c.new = True
            data = _dice_duel_data()
            for w in DiceDuelUserLimit.objects.all():
                if w.user.push_token and w.user.days_left() > 0:
                    for k, v in data.items():
                        if getattr(w, "{}_push".format(k)) and v >= getattr(w, k):
                            onesignal.to_users(w.user.push_token, w.user.sound, w.user.sound_name, u"Дуэль Костей", u"Дуэль Костей: {}".format(parser.DICE_DUEL_NAMES[k].lower()), u"Количество ходов уже: {}".format(v), k, 60)
        return len(new_uuids)
    return 0



@shared_task
def clear_data():
    """
    Celery task for parsing results of War of Bets game.
    Timezone is UTC
    :return:
    """
    prev = None
    dices = list()
    for w in DiceDuelUserLimit.objects.order_by('-user'):
        if prev and prev.user.pk == w.user.pk:
            dices.append(w)
        prev = w
    for b in dices:
        b.delete()
    prev = None
    wheels = list()
    for w in WheelUserLimit.objects.order_by('-user'):
        if prev and prev.user.pk == w.user.pk:
            wheels.append(w)
        prev = w
    for b in wheels:
        b.delete()
    prev = None
    pokers = list()
    for w in PokerUserLimit.objects.order_by('-user'):
        if prev and prev.user.pk == w.user.pk:
            pokers.append(w)
        prev = w
    for b in pokers:
        b.delete()
    prev = None
    warbets = list()
    for w in WarbetsUserLimit.objects.order_by('-user'):
        if prev and prev.user.pk == w.user.pk:
            warbets.append(w)
        prev = w
    for b in warbets:
        b.delete()
    prev = None
    baccarats = list()
    for w in BaccaratUserLimit.objects.order_by('-user'):
        if prev and prev.user.pk == w.user.pk:
            baccarats.append(w)
        prev = w
    for b in baccarats:
        b.delete()
