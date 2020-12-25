


def to_str(val):
    __halt_on_nonetype(val)

    if (__is_list(val) or 
        __is_dict(val) or 
        __is_bool(val) or
        __is_tuple(val)):
        raise TypeError(f"{type(val)} is an invalid datatype")
    
    return str(val)


def to_list(val):
    __halt_on_nonetype(val)

    if (__is_list(val) or
        __is_tuple(val)):
        return [to_str(v) for v in val]
    else:
        return [to_str(val)]


def __halt_on_nonetype(val):
    if __is_none(val):
        raise TypeError


def __is_list(val):
    if type(val) == list:
        return True
    else:
        return False


def __is_dict(val):
    if type(val) == dict:
        return True
    else:
        return False


def __is_tuple(val):
    if type(val) == tuple:
        return True
    else:
        return False


def __is_bool(val):
    if type(val) == bool:
        return True
    else:
        return False


def __is_none(val):
    if val is None:
        return True
    else:
        return False