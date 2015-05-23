
OPERATOR2 = ["+", "-", "*", "/",
        "%", "<", "<=", ">", ">=",
        "==", "!=", "**"]

OPERATOR1 = [
    "'+", "'-", "'~"
]

def vmap(f, dic):
    return dict(zip(dic.keys(), map(f, dic.values())))

def splitWhile(f, xs):
    for i in range(len(xs)):
        if (not f(xs[i])):
            return (xs[:i], xs[i:])
    return (xs, [])

def takeWhile(f, xs):
    return splitWhile(f, xs)[0]

def dropWhile(f, xs):
    return splitWhile(f, xs)[1]
    

class Formula(object):
    def __init__(self):
        pass

    def __str__(self):
        return Formula.parse(self.traverse())

    @classmethod
    def parse(cls, rpf):
        stack = []
        for t in rpf:
            if t in OPERATOR2:
                a = stack.pop()
                b = stack.pop()
                stack.append("({}{}{})".format(b, t, a))
            elif t in OPERATOR1:
                a = stack.pop()
                stack.append("{}{}".format(t[1:], a))
            elif isinstance(t, tuple):
                print t
                stack.append("___CONSTS___['{}']".format(t[0]))
            elif t.startswith("mc__"):
                args_count = int(takeWhile(lambda x: x.isdigit(), t[len("mc__"):]))
                args = [stack.pop() for i in range(args_count)]
                a = stack.pop()
                stack.append("{}.{}({})".format(
                    a,
                    dropWhile(lambda x: x.isdigit(), t[4:]),
                    ",".join(reversed(args))))
            else:
                stack.append(t)
        return stack[0]

    def create_lambda_string(self, rp_form):
        body = Formula.parse(rp_form)
        args = ",".join(["___CONSTS___"] + filter(lambda x: not isinstance(x, tuple) and x.startswith("___") and x.endswith("___"), rp_form))
        return "lambda {}:{}".format(args, body)

    def __call__(self, *args):
        c = [0]
        def us2args(x):
            if x == "___ARG___":
                k = c[0]
                c[0] += 1
                return "___ARG{}___".format(k)
            return x

        rp_form = map(us2args, self.traverse())
        lambda_string = self.create_lambda_string(rp_form)
        binds = filter(lambda x: isinstance(x, tuple), rp_form)
        ___CONSTS___ = dict(binds)
        print lambda_string
        print ___CONSTS___
        f = eval(lambda_string)
        return f(___CONSTS___, *args)
        

    def do_operator2(self, other, operator):
        if not issubclass(other.__class__, Formula):
            other = Operand(other)
        return Operator2(operator, self, other)

    def rdo_operator2(self, other, operator):
        if not issubclass(other.__class__, Formula):
            other = Operand(other)
        return Operator2(operator, other, self)

    def do_operator1(self, operator):
        return Operator1(operator, self)

    @classmethod
    def convert_oprand(cls, x):
        if not issubclass(x.__class__, Formula):
            return Operand(x)
        return x

    def do_methodcall(self, method):
        def f(*args, **kwargs):
            return MethodCall(self, method, 
                    map(Formula.convert_oprand, args),
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
        return self.do_operator2(other, "and")

    def __or__(self, other):
        return self.do_operator2(other, "or")

    def __xor__(self, other):
        return self.do_operator2(other, "xor")

    def __radd__(self, other):
        return self.rdo_operator2(other, "+")

    def __rsub__(self, other):
        return self.rdo_operator2(other, "-")

    def __rmul__(self, other):
        return self.rdo_operator2(other, "*")

    def __rdiv__(self, other):
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
        return self.rdo_operator2(other, "and")

    def __ror__(self, other):
        return self.rdo_operator2(other, "or")

    def __rxor__(self, other):
        return self.rdo_operator2(other, "xor")
#%}}}

    def __pos__(self):
        return self.do_operator1("+")

    def __neg__(self):
        return self.do_operator1("-")

    def __invert__(self):
        return self.do_operator1("~")

    def __getattr__(self, method):
        return self.do_methodcall(method)


class Operator1(Formula):
    def __init__(self, operator, value):
        self.operator = operator
        self.value = value

    def traverse(self):
        return self.value.traverse() + ["'" + self.operator]

class Operator2(Formula):
    def __init__(self, operator, left, right):
        self.operator = operator
        self.left = left
        self.right = right

    def traverse(self):
        return self.left.traverse() + self.right.traverse() + [self.operator]

n = 0
class Operand(Formula):
    def __init__(self, value):
        self.value = value

    def traverse(self):
        global n
        n += 1
        return [("CONST_{}".format(n), self.value)]

class MethodCall(Formula):
    def __init__(self,value,  method, args, kwargs):
        self.value = value
        self.method = method
        self.args = args
        self.kwargs = kwargs

    def traverse(self):
        return (self.value.traverse() + 
                reduce(lambda n, x: n + x.traverse(), self.args, [])
                + ["mc__{}".format(len(self.args)) + self.method])

class Const(Formula):
    def __init__(self, name):
        self.name = name

    def traverse(self):
        return ["__CONST{}__".format(self.name)]


class Underscore(Formula):

    def __init__(self):
        pass
    
    def traverse(self):
        return ["___ARG___"]

_ = Underscore()

if __name__ == '__main__':
    class ct:
        def test(self, a, b, c):
            return a + b + c + "___test"
    k = "nadeko"
    print (_ + _)(1, 2)
    print (_ + _ * _)(1, 2, 3)
    print (+_)(3)
    print (~_)(-1)
    print (-_)(3)
    print (_.test("test", k, "cute"))(ct())
    print (_.test(_ + _, _, _ * 2))(ct(), "test", "+nadeko", "____", "lambda")

