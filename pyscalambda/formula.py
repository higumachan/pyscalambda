
from utility import vmap


class Formula(object):
    @property
    def __name__(self):
        return self.get_lambda().__name__

    def __init__(self):
        self.is_cache = True
        self.cache_lambda = None
        self.cache_consts = None
        self.children = []

    def __str__(self):
        return self.create_lambda_string()

    def debug(self):
        return (self.create_lambda_string(), list(self.traverse_const_values()))

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

    def create_lambda(self):
        binds = self.traverse_const_values()
        lambda_string = self.create_lambda_string()
        return eval(lambda_string, dict(binds))

    def get_lambda(self):
        if not self.is_cache or self.cache_lambda is None:
            self.cache_lambda = self.create_lambda()
        return self.cache_lambda

    def __call__(self, *args):
        return self.get_lambda()(*args)

    @classmethod
    def convert_oprand(cls, x):
        from operands import ConstOperand, Underscore

        if not issubclass(x.__class__, Formula):
            return ConstOperand(x)
        if isinstance(x, Underscore) and x.id == 0:
            return Underscore()
        return x

    def do_operator2(self, other, operator):
        from operators import BinaryOperator

        this = Formula.convert_oprand(self)
        other = Formula.convert_oprand(other)
        return BinaryOperator(operator, this, other)

    def rdo_operator2(self, other, operator):
        from operators import BinaryOperator

        this = Formula.convert_oprand(self)
        other = Formula.convert_oprand(other)
        return BinaryOperator(operator, other, this)

    def do_operator1(self, operator):
        from operators import UnaryOperator

        this = Formula.convert_oprand(self)
        return UnaryOperator(operator, this)

    def do_getitem(self, item):
        from formula_nodes import GetItem

        this = Formula.convert_oprand(self)
        item = Formula.convert_oprand(item)
        return GetItem(this, item)

    def do_methodcall(self, method):
        from formula_nodes import MethodCall

        def f(*args, **kwargs):
            this = Formula.convert_oprand(self)
            return MethodCall(
                this,
                method,
                list(map(Formula.convert_oprand, args)),
                vmap(Formula.convert_oprand, kwargs)
            )
        return f

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
