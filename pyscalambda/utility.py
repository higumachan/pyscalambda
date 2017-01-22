def vmap(f, dic):
    return dict(zip(dic.keys(), map(f, dic.values())))


def can_str_emmbed(value):
    return isinstance(value, (int, str, float))


def str_emmbed(value):
    return "'{}'".format(value) if isinstance(value, str) else str(value)


def convert_operand(x):
    from pyscalambda.operands import ConstOperand, Underscore
    from pyscalambda.formula import Formula

    if not issubclass(x.__class__, Formula):
        return ConstOperand(x)
    if isinstance(x, Underscore) and x.id == 0:
        return Underscore()
    return x
