from common.constants import TRUE_VALUES, FALSE_VALUES, NULL_VALUES


def string_to_bool(value):
    if value in TRUE_VALUES:
        return True
    elif value in FALSE_VALUES:
        return False
    if value in NULL_VALUES:
        return None
    return bool(value)


def int_or_zero(value):
    try:
        return int(value)
    except ValueError:
        return 0
