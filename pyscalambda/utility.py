def vmap(f, dic):
    return dict(zip(dic.keys(), map(f, dic.values())))


def can_str_emmbed(value):
    return isinstance(value, (int, str, float))


def str_emmbed(value):
    return "'{}'".format(value) if isinstance(value, str) else str(value)
