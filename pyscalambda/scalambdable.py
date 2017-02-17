import functools

from pyscalambda.formula_nodes import FunctionCall, MakeDictionary, MakeIterator

from pyscalambda.operands import ConstOperand

from pyscalambda.utility import convert_operand, is_scalambda_object, is_unnamed_underscore, vmap


def scalambdable_func(fn, *funcs):
    """
    Wrap function to scalambdable.

    :type fn: (T)->U
    :type funcs: ((Any)->Any, ...)
    :rtype: (T)->U
    """
    def wrapped(*args, **kwargs):
        for f in reversed((fn,) + funcs):
            if any(map(is_scalambda_object, args)) or any(map(is_scalambda_object, kwargs.values())):
                args = [FunctionCall(f, list(map(convert_operand, args)), vmap(convert_operand, kwargs))]
                kwargs = {}
            else:
                args = [f(*args, **kwargs)]
                kwargs = {}
        return args[0]
    return wrapped if funcs else functools.wraps(fn)(wrapped)


def validate_unorderd(iter):
    if isinstance(iter, set) and any(map(is_unnamed_underscore, iter)):
        return False, ["set is unorderd", "using unnamed underscore(You can use _1 to _9)"]
    if (isinstance(iter, dict) and
            (any(map(is_unnamed_underscore, iter.keys())) or any(map(is_unnamed_underscore, iter.values())))):
        return False, ["dict is unorderd", "using unnamed underscore(You can use _1 to _9)"]
    return True, []


def scalambdable_iterator(iter):
    wrappers = {
        list: ('[', ']'),
        tuple: ('(', ')'),
        set: ('{', '}'),
    }

    valid, reasons = validate_unorderd(iter)
    if not valid:
        raise SyntaxError("Can't decide lambda unnamed argument order. Because {}".format(" and ".join(reasons)))

    if isinstance(iter, (list, tuple, set)):
        iter_type = type(iter)
        iter = map(convert_operand, iter)
        return MakeIterator(iter, *wrappers[iter_type])

    keys = map(convert_operand, iter.keys())
    values = map(convert_operand, iter.values())
    return MakeDictionary(keys, values)


def scalambdable_const(value):
    return ConstOperand(value)
