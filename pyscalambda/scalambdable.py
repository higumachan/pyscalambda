import functools

from formula import Formula

from formula_nodes import FunctionCall

from utility import convert_oprand, vmap


def scalambdable_func(*funcs):
    @functools.wraps(funcs[0])
    def wraps(*args, **kwargs):
        for f in reversed(funcs):
            def is_scalambda_object(x):
                return issubclass(x.__class__, Formula)
            if any(map(is_scalambda_object, args)) or any(map(is_scalambda_object, kwargs.values())):
                args = [FunctionCall(f, list(map(convert_oprand, args)), vmap(convert_oprand, kwargs))]
                kwargs = {}
            else:
                args = [f(*args, **kwargs)]
                kwargs = {}
        return args[0]
    return wraps
