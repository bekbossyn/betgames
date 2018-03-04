# -*- coding: utf-8 -*-
from lxml import html
import requests

BACCARAT_URL = 'https://olimp.betgames.tv/ext/game/results/olimp/{}-{}-{}/6'
POKER_URL = 'https://olimp.betgames.tv/ext/game/results/olimp/{}-{}-{}/5'
WARBETS_URL = 'https://olimp.betgames.tv/ext/game/results/olimp/{}-{}-{}/8'
WHEEL_URL = 'https://olimp.betgames.tv/ext/game/results/olimp/{}-{}-{}/7'
DICE_DUEL_URL = 'https://olimp.betgames.tv/ext/game/results/olimp/{}-{}-{}/10'


def _prettify_result(res):
    return [s.strip() for s in res.split(',')]


def _prettify_poker_result(res):
    return " ".join([s.strip() for s in res])


def _prettify_id(id):
    return {
        "timestamp": id.split(' - ')[0],
        "id": id.split(' - ')[1],
    }


def get_baccarat(year, month, day):
    if month < 10:
        month = "0{}".format(month)
    if day < 10:
        day = "0{}".format(day)
    result = list()
    page = requests.get(BACCARAT_URL.format(year, month, day))
    tree = html.fromstring(page.content)
    tbody = tree.xpath('//*[@id="table"]/table/tbody/tr')
    for i, tr in enumerate(tbody):
        # print(i)
        # print(tr.xpath('td[1]/text()')[0])
        obj = dict()
        obj['id'] = _prettify_id(tr.xpath('td[1]/text()')[0])['id']
        obj['timestamp'] = _prettify_id(tr.xpath('td[1]/text()')[0])['timestamp']
        # //*[@id="table"]/table/tbody/tr[1]/td[3]/span[1]
        # //*[@id="table"]/table/tbody/tr[2]/td[3]/span[2]
        player = False
        banker = False
        if 'winner' in tr.xpath('td[3]/span')[0].get('class'):
            player = True
        elif 'winner' in tr.xpath('td[3]/span')[1].get('class'):
            banker = True
        if tr.xpath('td[3]/span[3]/text()')[0] == 'Tie':
            # print("YES")
            # print(tr.xpath('td[3]/span[4]/span/text()'))
            # print(_prettify_result(tr.xpath('td[3]/span[4]/span/text()')[0]))
            obj['result'] = _prettify_result(tr.xpath('td[3]/span[4]/span/text()')[0]) + ["Tie"]
        else:
            obj['result'] = _prettify_result(tr.xpath('td[3]/span[3]/span/text()')[0])
        if player:
            obj['result'] = obj['result'] + ["Player"]
        if banker:
            obj['result'] = obj['result'] + ["Banker"]
        result.append(obj)
    return result


def get_poker(year, month, day):
    if month < 10:
        month = "0{}".format(month)
    if day < 10:
        day = "0{}".format(day)
    result = list()
    page = requests.get(POKER_URL.format(year, month, day))
    tree = html.fromstring(page.content)
    tbody = tree.xpath('//*[@id="table"]/table/tbody/tr')
    for i, tr in enumerate(tbody):
        obj = dict()
        obj['id'] = _prettify_id(tr.xpath('td[1]/text()')[0])['id']
        if obj['id'] == "31707030047":
            print("YES")
        obj['timestamp'] = _prettify_id(tr.xpath('td[1]/text()')[0])['timestamp']
        obj['hand'] = _prettify_poker_result(tr.xpath('td[3]/div[2]/span/text()'))
        obj['result'] = _prettify_poker_result(tr.xpath('td[3]/div[2]/text()')).lower()
        result.append(obj)
    return result


def get_warbets(year, month, day):
    if month < 10:
        month = "0{}".format(month)
    if day < 10:
        day = "0{}".format(day)
    result = list()
    page = requests.get(WARBETS_URL.format(year, month, day))
    tree = html.fromstring(page.content)
    tbody = tree.xpath('//*[@id="table"]/table/tbody/tr')
    for i, tr in enumerate(tbody):
        obj = dict()
        obj['id'] = _prettify_id(tr.xpath('td[1]/text()')[0])['id']
        player_class = tr.xpath('td[3]/span[1]/span[2]/@class')
        diller_class = tr.xpath('td[3]/span[2]/span[2]/@class')
        rplayer_class = tr.xpath('td[3]/span[1]/@class')
        rdiller_class = tr.xpath('td[3]/span[2]/@class')
        obj['player_red'] = 'hearts' in player_class[0].lower() or 'diamonds' in player_class[0].lower()
        obj['diller_red'] = 'hearts' in diller_class[0].lower() or 'diamonds' in diller_class[0].lower()
        obj['player_win'] = 'winner' in rplayer_class[0].lower()
        obj['diller_win'] = 'winner' in rdiller_class[0].lower()
        obj['timestamp'] = _prettify_id(tr.xpath('td[1]/text()')[0])['timestamp']
        result.append(obj)
    return result


def get_wheel(year, month, day):
    if month < 10:
        month = "0{}".format(month)
    if day < 10:
        day = "0{}".format(day)
    result = list()
    page = requests.get(WHEEL_URL.format(year, month, day))
    tree = html.fromstring(page.content)
    tbody = tree.xpath('//*[@id="table"]/table/tbody/tr')
    for i, tr in enumerate(tbody):
        obj = dict()
        obj['id'] = _prettify_id(tr.xpath('td[1]/text()')[0])['id']
        obj['number'] = int(tr.xpath('td[3]/span/span/text()')[0].strip())
        obj['color'] = tr.xpath('td[3]/span/@class')[0]
        obj['timestamp'] = _prettify_id(tr.xpath('td[1]/text()')[0])['timestamp']
        result.append(obj)
    return result


def get_dice_duel(year, month, day):
    if month < 10:
        month = "0{}".format(month)
    if day < 10:
        day = "0{}".format(day)
    result = list()
    page = requests.get(DICE_DUEL_URL.format(year, month, day))
    tree = html.fromstring(page.content)
    tbody = tree.xpath('//*[@id="table"]/table/tbody/tr')
    for i, tr in enumerate(tbody):
        obj = dict()
        obj['id'] = _prettify_id(tr.xpath('td[1]/text()')[0])['id']
        red_class = tr.xpath('td[3]/span[1]/@class')[0]
        blue_class = tr.xpath('td[3]/span[2]/@class')[0]
        if 'dice-1' in red_class: red = 1
        if 'dice-2' in red_class: red = 2
        if 'dice-3' in red_class: red = 3
        if 'dice-4' in red_class: red = 4
        if 'dice-5' in red_class: red = 5
        if 'dice-6' in red_class: red = 6
        if 'dice-1' in blue_class: blue = 1
        if 'dice-2' in blue_class: blue = 2
        if 'dice-3' in blue_class: blue = 3
        if 'dice-4' in blue_class: blue = 4
        if 'dice-5' in blue_class: blue = 5
        if 'dice-6' in blue_class: blue = 6
        obj['red'] = red
        obj['blue'] = blue
        obj['timestamp'] = _prettify_id(tr.xpath('td[1]/text()')[0])['timestamp']
        result.append(obj)
    return result


POKER_NAMES = {
    "one_pair": u"ОДНА ПАРА",
    "two_pairs": u"ДВЕ ПАРЫ",
    "three_of_a_kind": u"СЕТ",
    "flush": u"ФЛЭШ",
    "straight": u"СТРИТ",
    "full_house": u"ФУЛ-ХАУС",
    "four_of_a_kind": u"КАРЕ"
}


BACCARAT_NAMES = {
    "player": u"ИГРОК",
    "banker": u"БАНКИР",
    "tie": u"НИЧЬЯ",
    "either_pair": u"ЛЮБАЯ ПАРА",
    "big": u"БОЛЬШАЯ",
    "small": u"МАЛАЯ"
}


WARBETS_NAMES = {
    "player": u"Игрок",
    "diller": u"Дилер",
    "draw": u"Ничья",
    "player_red": u"Игрок Красный",
    "player_black": u"Игрок Черный",
    "diller_red": u"Дилер Красный",
    "diller_black": u"Дилер Черный",
    "just_black": u"Общий Черный",
    "just_red": "Общий Красный"
}


WHEEL_NAMES = {
    "d1_to_d6": u"Число от 1 до 6",
    "d7_to_d12": u"Число от 7 до 12",
    "d13_to_d18": u"Число от 13 до 18",
    "less": u"Меньше 9.5",
    "more": u"Больше 9.5",
    "grey": u"Серый",
    "red": u"Красный",
    "black": u"Черный",
    "even": u"Четное",
    "odd": u"Нечетное"
}


DICE_DUEL_NAMES = {
    "red_win": u"Победа КРАСНАЯ",
    "blue_win": u"Победа СИНЯЯ",
    "draw": u"Ничья"
}
