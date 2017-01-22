import functools

from pyscalambda.formula import Formula

from pyscalambda.formula_nodes import FunctionCall

from pyscalambda.utility import convert_oprand, vmap


def scalambdable_func(fn, *funcs):
    @functools.wraps(fn)
    def wraps(*args, **kwargs):
        for f in reversed([fn] + funcs):
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
