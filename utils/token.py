import jwt
from django.conf import settings
from django.contrib.auth import get_user_model

from main.models import TokenLog, MyUser
import time

User = get_user_model()


def create_token(user):
    """
    Creates token string.
    :param user: User for which token should be created.
    :return: authentication token.
    """
    info = {
        'id': user.id,
        'phone': user.email,
        'timestamp': time.time()
    }
    token = jwt.encode(info, settings.JWT_KEY, settings.JWT_ALGORITHM).decode('utf-8')
    TokenLog.objects.filter(user=user, deleted=False).update(deleted=True)
    TokenLog.objects.create(user=user, token=token)
    return token


def verify_token(token_string):
    """
    Verifies token string.

    :param token_string: Token string to verify.
    :return: Profile/user object if token is valid; None is token is invalid.
    """
    try:
        result = jwt.decode(token_string, settings.JWT_KEY, settings.JWT_ALGORITHM)
        user_id = result['id']
        phone = result['phone']
        user = User.objects.get(id=user_id)
        user.tokens.get(token=token_string, deleted=False)
        if user.email != phone:
            return None
        return user
    except Exception as e:
        return None
