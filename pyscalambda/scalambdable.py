import functools

from pyscalambda.formula import Formula

from pyscalambda.formula_nodes import FunctionCall

from pyscalambda.utility import convert_operand, vmap


def scalambdable_func(fn, *funcs):
    """
    Wrap function to scalambdable.

    :type fn: (T)->U
    :type funcs: ((Any)->Any, ...)
    :rtype: (T)->U
    """
    def wrapped(*args, **kwargs):
        for f in reversed((fn,) + funcs):
            def is_scalambda_object(x):
                return issubclass(x.__class__, Formula)
            if any(map(is_scalambda_object, args)) or any(map(is_scalambda_object, kwargs.values())):
                args = [FunctionCall(f, list(map(convert_operand, args)), vmap(convert_operand, kwargs))]
                kwargs = {}
            else:
                args = [f(*args, **kwargs)]
                kwargs = {}
        return args[0]
    return wrapped if funcs else functools.wraps(fn)(wrapped)
