import re


def empty_to_none(s):
    """
    :param s: String to be converted.
    :return: If string is empty returns None; otherwise returns string itself.
    """
    if s is not None:
        if len(s) == 0:
            return None
    return s


def integer_list(_list):
    return map(int, _list)


def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def isEnglish(s):
    try:
        s.decode('ascii')
    except UnicodeDecodeError:
        return False
    else:
        return True


def valid_phone(phone):
    phone = re.sub("[^0-9]", "", phone)
    if len(phone) >= 10 and len(phone) <= 13:
        return True, "+" + phone
    return False, None
