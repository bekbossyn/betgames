# -*- coding: utf-8 -*-
import requests
import json

one_signal_header = {
    "Content-Type": "application/json; charset=utf-8",
    "Authorization": "Basic YTRiYzg3MzMtYTQyNi00ODkzLWI2NWUtYTc2MGY3MWRjMzZj"
}

one_signal_payload = {
    "app_id": "06b21819-8732-490a-b98f-54feba27ca39",
    "include_player_ids": [""],
    "contents": {
        "en": u"BetMates"
    },
    "headings": {
        "en": u"BetMates"
    },
    "priority": 10,
    "android_sound": "onesignal",
    "large_icon": "ic_onesignal",
    "small_icon": "ic_onesignal"
}


def to_users(token, sound, sound_name, group, heading, message, param_name, ttl, data=None):
    if not data:
        data = {
            "is_test": False
        }
    one_signal_payload["include_player_ids"] = [token]
    one_signal_payload["collapse_id"] = param_name
    one_signal_payload["android_group"] = group
    one_signal_payload["ttl"] = ttl
    one_signal_payload["headings"]["en"] = heading
    one_signal_payload["contents"]["en"] = message
    one_signal_payload["data"] = data
    if not sound:
        one_signal_payload["android_sound"] = "nil"
    else:
        one_signal_payload["android_sound"] = sound_name
    try:
        requests.post("https://onesignal.com/api/v1/notifications", headers=one_signal_header, data=json.dumps(one_signal_payload))
    except Exception as e:
        pass
