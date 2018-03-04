# -*- coding: utf-8 -*-
from datetime import timedelta

from django.conf import settings
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from main.tasks import baccarat, poker, warbets, wheel, dice_duel, email
from main.models import Activation

from utils import http, codes, token
from utils.string_utils import valid_phone


User = get_user_model()


def index(request):
    dice_duel()
    return HttpResponse("OK 2.0")


def test_500(request):
    a = dict()
    a['test'][0] = 0
    return HttpResponse("OK 2.0")


@http.json_response()
@http.requires_token()
@csrf_exempt
def get_info(request, user):
    return {
        "user": user.json()
    }


@http.json_response()
@http.required_methods("POST")
@http.required_parameters(["phone"])
@csrf_exempt
def register(request):
    return http.code_response(code=codes.OK)


@http.json_response()
@http.required_methods("POST")
@http.required_parameters(["phone"])
@csrf_exempt
def phone_login(request):
    valid, phone = valid_phone(request.POST["phone"])
    if not valid:
        return http.code_response(code=codes.BAD_REQUEST, message=u"Неверный формат телефона")
    Activation.objects.filter(phone=phone, used=False).update(used=True)
    Activation.objects.create_code(phone)
    return http.code_response(code=codes.OK)


@http.json_response()
@http.required_methods("POST")
@http.required_parameters(["phone", "code"])
@csrf_exempt
def phone_login_complete(request):
    valid, phone = valid_phone(request.POST["phone"])
    if not valid:
        return http.code_response(code=codes.BAD_REQUEST, message=u"Неверный формат телефона")
    try:
        activation = Activation.objects.filter(phone=phone, code=request.POST.get('code', ''), used=False)[0]
    except:
        return http.code_response(code=codes.BAD_REQUEST, message=u"Неверный ключ активации")
    u, _ = User.objects.get_or_create(email=activation.phone)
    if not u.tariff_date:
        u.tariff_date = timezone.now().date() + timedelta(days=0)
        u.tariff = User.DEMO
    u.save()
    activation.used = True
    activation.save()

    try:
        email.delay(settings.ADMINS_LIST,
                    u"Новый пользователь #{}".format(u.phone),
                    u"Новый пользователь под номером {} и ID {}".format(u.phone, u.pk))
    except:
        pass

    return {
        'token': token.create_token(u),
        'user': u.json()
    }
