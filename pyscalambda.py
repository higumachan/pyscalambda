from __future__ import print_function

import functools


def vmap(f, dic):
    return dict(zip(dic.keys(), map(f, dic.values())))

class Formula(object):
    def __init__(self):
        self.is_cache = True
        self.cache_lambda = None
        self.cache_consts = None
        self.children = []

    def __str__(self):
        return self.create_lambda_string()

    def debug(self):
        print(self.create_lambda_string())
        print(list(self.traverse_const_values()))


    def nocache(self):
        self.is_cache = False
        return self

    def create_lambda_string(self):
        traversed = list(self.traverse())
        body = "".join(traversed)

        constized_args = sorted(list(set(self.traverse_constize_args())))
        unnamed_args = list(self.traverse_args())
        if len(constized_args) == 0:
            args = ",".join(unnamed_args)
        elif len(unnamed_args) == 0:
            args = ",".join(constized_args)
        else:
            raise SyntaxError("_ and _1 ~ _9 can not be used at the same time.")
        return "lambda {}:{}".format(args, body)

    def __call__(self, *args) :
        if not self.is_cache or self.cache_lambda is None:
            binds = self.traverse_const_values()
            lambda_string = self.create_lambda_string()
            self.cache_lambda = eval(lambda_string, dict(binds))
        return self.cache_lambda(*args)

    @classmethod
    def convert_oprand(cls, x):
        if not issubclass(x.__class__, Formula):
            return ConstOperand(x)
        if isinstance(x, Underscore) and x.id == 0:
            return Underscore()
        return x

    def do_operator2(self, other, operator):
        this = Formula.convert_oprand(self)
        other = Formula.convert_oprand(other)
        return Operator2(operator, this, other)

    def rdo_operator2(self, other, operator):
        this = Formula.convert_oprand(self)
        other = Formula.convert_oprand(other)
        return Operator2(operator, other, this)

    def do_operator1(self, operator):
        this = Formula.convert_oprand(self)
        return Operator1(operator, this)

    def do_getitem(self, item):
        this = Formula.convert_oprand(self)
        item = Formula.convert_oprand(item)
        return GetItem(this, item)

    def do_methodcall(self, method):
        def f(*args, **kwargs):
            this = Formula.convert_oprand(self)
            return MethodCall(this, method,
                    list(map(Formula.convert_oprand, args)),
                    vmap(Formula.convert_oprand, kwargs))
        return f

#%{{{
    def __add__(self, other):
        return self.do_operator2(other, "+")

    def __sub__(self, other):
        return self.do_operator2(other, "-")

    def __mul__(self, other):
        return self.do_operator2(other, "*")

    def __div__(self, other):
        return self.do_operator2(other, "/")

    def __truediv__(self, other):
        return self.do_operator2(other, "/")

    def __floordiv__(self, other):
        return self.do_operator2(other, "//")

    def __mod__(self, other):
        return self.do_operator2(other, "%")

    def __lt__(self, other):
        return self.do_operator2(other, "<")

    def __le__(self, other):
        return self.do_operator2(other, "<=")

    def __gt__(self, other):
        return self.do_operator2(other, ">")

    def __ge__(self, other):
        return self.do_operator2(other, ">=")

    def __eq__(self, other):
        return self.do_operator2(other, "==")

    def __ne__(self, other):
        return self.do_operator2(other, "!=")

    def __pow__(self, other):
        return self.do_operator2(other, "**")

    def __lshift__(self, other):
        return self.do_operator2(other, "<<")

    def __rshift__(self, other):
        return self.do_operator2(other, ">>")

    def __and__(self, other):
        return self.do_operator2(other, "&")

    def __or__(self, other):
        return self.do_operator2(other, "|")

    def __xor__(self, other):
        return self.do_operator2(other, "^")

    def __radd__(self, other):
        return self.rdo_operator2(other, "+")

    def __rsub__(self, other):
        return self.rdo_operator2(other, "-")

    def __rmul__(self, other):
        return self.rdo_operator2(other, "*")

    def __rdiv__(self, other):
        return self.rdo_operator2(other, "/")

    def __rtruediv__(self, other):
        return self.rdo_operator2(other, "/")

    def __rfloordiv__(self, other):
        return self.rdo_operator2(other, "//")

    def __rmod__(self, other):
        return self.rdo_operator2(other, "%")

    def __rlt__(self, other):
        return self.rdo_operator2(other, "<")

    def __rle__(self, other):
        return self.rdo_operator2(other, "<=")

    def __rgt__(self, other):
        return self.rdo_operator2(other, ">")

    def __rge__(self, other):
        return self.rdo_operator2(other, ">=")

    def __req__(self, other):
        return self.rdo_operator2(other, "==")

    def __rne__(self, other):
        return self.rdo_operator2(other, "!=")

    def __rpow__(self, other):
        return self.rdo_operator2(other, "**")

    def __rlshift__(self, other):
        return self.rdo_operator2(other, "<<")

    def __rrshift__(self, other):
        return self.rdo_operator2(other, ">>")

    def __rand__(self, other):
        return self.rdo_operator2(other, "&")

    def __ror__(self, other):
        return self.rdo_operator2(other, "|")

    def __rxor__(self, other):
        return self.rdo_operator2(other, "^")
#%}}}

    def __pos__(self):
        return self.do_operator1("+")

    def __neg__(self):
        return self.do_operator1("-")

    def __invert__(self):
        return self.do_operator1("~")

    def __getattr__(self, method):
        return self.do_methodcall(method)

    def __getitem__(self, key):
        return self.do_getitem(key)

    def traverse_const_values(self):
        for child in self.children:
            for t in child.traverse_const_values():
                yield t

    def traverse_args(self):
        for child in self.children:
            for t in child.traverse_args():
                yield t

    def traverse_constize_args(self):
        for child in self.children:
            for t in child.traverse_constize_args():
                yield t


class Operator(Formula):
    pass


class Operator1(Operator):
    def __init__(self, operator, value):
        super(Operator1, self).__init__()
        self.operator = operator
        self.value = value
        self.children = [self.value]

    def traverse(self):
        yield '('
        yield self.operator
        for t in self.value.traverse():
            yield t
        yield ')'


class Operator2(Operator):
    def __init__(self, operator, left, right):
        super(Operator2, self).__init__()
        self.operator = operator
        self.left = left
        self.right = right
        self.children = [self.left, self.right]

    def traverse(self):
        yield '('
        for t in self.left.traverse():
            yield t
        yield self.operator
        for t in self.right.traverse():
            yield t
        yield ')'


class Operand(Formula):
    pass


class ConstOperand(Operand):
    COUNTER = 0

    def __init__(self, value):
        super(ConstOperand, self).__init__()
        self.id = ConstOperand.COUNTER
        ConstOperand.COUNTER += 1
        self.value = value

    def traverse(self):
        yield '('
        yield "CONST_{}".format(self.id)
        yield ')'

    def traverse_const_values(self):
        yield ('CONST_{}'.format(self.id), self.value)


class Underscore(Operand):
    NUMBER_CONSTIZE = 10
    COUNTER = NUMBER_CONSTIZE

    def __init__(self, id=None):
        super(Underscore, self).__init__()
        if id is None:
            self.id = Underscore.COUNTER
            Underscore.COUNTER += 1
        else:
            self.id = id

    def traverse(self):
        yield '('
        yield "___ARG{}___".format(self.id)
        yield ')'

    def traverse_args(self):
        if self.id >= Underscore.NUMBER_CONSTIZE:
            yield "___ARG{}___".format(self.id)

    def traverse_constize_args(self):
        if self.id < Underscore.NUMBER_CONSTIZE:
            yield "___ARG{}___".format(self.id)



class MethodCall(Formula):
    def __init__(self, value,  method, args, kwargs):
        super(MethodCall, self).__init__()
        self.value = value
        self.method = method
        self.args = args
        self.kwargs = kwargs
        self.children = [self.value] + self.args + list(self.kwargs.values())

    def traverse(self):
        yield '('
        for t in self.value.traverse():
            yield t
        yield '.'
        yield self.method
        yield '('
        for arg in self.args:
            for t in arg.traverse():
                yield t
            yield ','
        for name, arg in self.kwargs:
            yield '{}='.format(name)
            for t in self.arg.traverse():
                yield t
            yield ','
        yield ')'
        yield ')'


class GetItem(Formula):
    def __init__(self, value, item):
        super(GetItem, self).__init__()
        self.value = value
        self.item = item
        self.children = [self.value, self.item]

    def traverse(self):
        yield '('
        for t in self.value.traverse():
            yield t
        yield '['
        for t in self.item.traverse():
            yield t
        yield ']'
        yield ')'


class FunctionCall(Formula):
    COUNTER = 0

    def __init__(self, func, args, kwargs):
        super(FunctionCall, self).__init__()
        self.id = FunctionCall.COUNTER 
        FunctionCall.COUNTER += 1
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.children = self.args + list(self.kwargs.values())

    def traverse(self):
        yield "BIND_FUNC_{}".format(self.id)
        yield '('
        for arg in self.args:
            for t in arg.traverse():
                yield t
            yield ','
        for name, arg in self.kwargs:
            yield '{}='.format(name)
            for t in arg.traverse():
                yield t
            yield ','
        yield ')'

    def traverse_const_values(self):
        yield ('BIND_FUNC_{}'.format(self.id), self.func)
        for t in super(FunctionCall, self).traverse_const_values():
            yield t



def scalambdable_func(f):
    @functools.wraps(f)
    def wraps(*args, **kwargs):
        if any(map(lambda x: issubclass(x.__class__, Formula), args)) or any(map(lambda x: issubclass(x.__class__, Formula), kwargs.values())):
            return FunctionCall(f, list(map(Formula.convert_oprand, args)), vmap(Formula.convert_oprand, kwargs))
        return f(*args, **kwargs)
    return wraps

_ = Underscore(0)
_1 = Underscore(1)
_2 = Underscore(2)
_3 = Underscore(3)
_4 = Underscore(4)
_5 = Underscore(5)
_6 = Underscore(6)
_7 = Underscore(7)
_8 = Underscore(8)
_9 = Underscore(9)
SF = scalambdable_func

