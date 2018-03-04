import json

from datetime import datetime, timedelta

import requests
from django.conf import settings

from utils import codes


def send_sms(number, text):
    """
    Send SMS via mobizon.kz service.
    """
    values = {
        'apiKey': settings.SMS_MOBIZON_KEY,
        'recipient': number,
        'text': text,
        'output': 'json',
        'api': 'v1'
    }
    try:
        r = requests.post(settings.SMS_SEND_URL, data=values)
        return r.json()
    except Exception as e:
        return {
            "code": 999,
            "message": str(e)
        }
