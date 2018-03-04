import json
from functools import wraps

from django.conf import settings
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from six import string_types

from utils import codes
from utils import token
from utils.messages import *

User = get_user_model()


from . import string_utils


def required_methods(methods):
    """
    Decorator to make a view only accept request with required request methods.
    :param methods: list of required parameters.
    """
    def decorator(func):
        @wraps(func)
        def inner(request, *args, **kwargs):
            if isinstance(methods, string_types):
                if methods == request.method:
                    return func(request, *args, **kwargs)
            elif request.method in methods:
                return func(request, *args, **kwargs)
            return code_response(codes.BAD_REQUEST, message=u"METHOD NOT ALLOWED")
        return inner
    return decorator


def required_parameters(parameters_list):
    """
    Decorator to make a view only accept request with required parameters.
    :param parameters_list: list of required parameters.
    """
    def decorator(func):
        @wraps(func)
        def inner(request, *args, **kwargs):
            if request.method == "POST":
                for parameter in parameters_list:
                    value = string_utils.empty_to_none(request.POST.get(parameter) or request.FILES.get(parameter))
                    if value is None:
                        return code_response(codes.BAD_REQUEST, message=MISSING_REQUIRED_PARAMS + " " + parameter)
            else:
                for parameter in parameters_list:
                    value = string_utils.empty_to_none(request.GET.get(parameter))
                    if value is None:
                        return code_response(codes.BAD_REQUEST, message=MISSING_REQUIRED_PARAMS + " " + parameter)

            return func(request, *args, **kwargs)
        return inner
    return decorator


def login_required():
    """
    Decorator to make a view only accept request with valid token.
    """
    def decorator(func):
        @wraps(func)
        def inner(request, *args, **kwargs):
            if not request.user.is_authenticated():
                return code_response(codes.BAD_CREDITENTIALS)
            return func(request, *args, **kwargs)
        return inner
    return decorator


def http_response_with_json_body(body):
    return HttpResponse(body, content_type="application/json")


def http_response_with_json(json_object):
    return http_response_with_json_body(json.dumps(json_object))


def json_response():
    """
    Decorator that wraps response into json.
    """
    def decorator(func):

        @wraps(func)
        def inner(*args, **kwargs):
            response = func(*args, **kwargs)
            if not ('code' in response):
                response['code'] = codes.OK
            return http_response_with_json(response)

        return inner
    return decorator


def code_response(code, message=None):
    result = {'code': code}
    if message:
        result['message'] = message
    return result


def ok_response():
    return code_response(codes.OK)


def extract_token_from_request(request):
    """
    Extracts token string from request. First tries to get it from AUTH_TOKEN header,
    if not found (or empty) tries to get from cookie.
    :param request:
    :return: Token string found in header or cookie; null otherwise.
    """
    header_names_list = settings.AUTH_TOKEN_HEADER_NAME
    token_string = None
    for name in header_names_list:
        if name in request.META:
            token_string = string_utils.empty_to_none(request.META[name])

    if token_string is None:
        token_string = request.COOKIES.get(settings.AUTH_TOKEN_COOKIE_NAME, None)

    return string_utils.empty_to_none(token_string)


def requires_token():
    """
    Decorator to make a view only accept request with valid token.
    """
    def decorator(func):
        @wraps(func)
        def inner(request, *args, **kwargs):
            token_string = extract_token_from_request(request)
            if token_string is None:
                return code_response(codes.BAD_REQUEST)

            user = token.verify_token(token_string)
            if user is None:
                return code_response(codes.BAD_CREDITENTIALS)

            return func(request, user, *args, **kwargs)
        return inner
    return decorator
