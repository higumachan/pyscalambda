from pyscalambda.utility import convert_operand, vmap


class BaseFormula(object):
    def do_operator2(self, other, operator):
        from pyscalambda.operators import BinaryOperator

        this = convert_operand(self)
        other = convert_operand(other)
        return BinaryOperator(operator, this, other)

    def rdo_operator2(self, other, operator):
        from pyscalambda.operators import BinaryOperator

        this = convert_operand(self)
        other = convert_operand(other)
        return BinaryOperator(operator, other, this)

    def do_operator1(self, operator):
        from pyscalambda.operators import UnaryOperator

        this = convert_operand(self)
        return UnaryOperator(operator, this)

    def do_getitem(self, item):
        from pyscalambda.formula_nodes import GetItem

        this = convert_operand(self)
        item = convert_operand(item)
        return GetItem(this, item)

    def do_methodcall(self, method):
        from pyscalambda.formula_nodes import MethodCall

        def f(*args, **kwargs):
            this = convert_operand(self)
            return MethodCall(
                this,
                method,
                list(map(convert_operand, args)),
                vmap(convert_operand, kwargs)
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
