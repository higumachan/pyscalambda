import functools
OPERATOR2 = ["+", "-", "*", "/",
        "%", "<", "<=", ">", ">=",
        "==", "!=", "**", "&", "|", "^"]

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
        self.cache_lambda = None
        self.cache_consts = None

    def __str__(self):
        rp_form = self.create_reverse_polish_nation()
        return self.create_lambda_string(rp_form)

    @classmethod
    def parse(cls, rpf):
        def get_args_count(t, prefix):
            return int(takeWhile(lambda x: x.isdigit(), t[len(prefix):]))

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
                if (t[0].startswith("BINDFUNC_")):
                    args_count = t[2]
                    args = [stack.pop() for i in range(args_count)]
                    stack.append("___CONSTS___['{}']({})".format(
                        t[0],
                        ",".join(reversed(args)),
                        ))
                else:
                    stack.append("___CONSTS___['{}']".format(t[0]))
            elif t.startswith("mc__"):
                args_count = get_args_count(t, "mc__")
                args = [stack.pop() for i in range(args_count)]
                a = stack.pop()
                stack.append("{}.{}({})".format(
                    a,
                    dropWhile(lambda x: x.isdigit(), t[4:]),
                    ",".join(reversed(args))))
            elif t == "__gi__":
                d = stack.pop()
                key = stack.pop()
                stack.append("{}[{}]".format(key, d))
            else:
                stack.append(t)
        return stack[0]

    def create_reverse_polish_nation(self):
        c = [0]
        def us2args(x):
            if x == "___ARG___":
                k = c[0]
                c[0] += 1
                return "___ARG{}___".format(k)
            return x
        return map(us2args, self.traverse())


    def create_lambda_string(self, rp_form):
        body = Formula.parse(rp_form)
        args = ",".join(["___CONSTS___"] + filter(lambda x: not isinstance(x, tuple) and x.startswith("___") and x.endswith("___"), rp_form))
        return "lambda {}:{}".format(args, body)

    def __call__(self, *args):
        if self.cache_lambda == None:
            rp_form = self.create_reverse_polish_nation()
            binds = map(lambda x: (x[0], x[1]) if len(x) == 3 else x, filter(lambda x: isinstance(x, tuple), rp_form))
            self.cache_consts = dict(binds)
            lambda_string = self.create_lambda_string(rp_form)
            self.cache_lambda = eval(lambda_string)
        return self.cache_lambda(self.cache_consts, *args)


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

    def do_getitem(self, item):
        if not issubclass(item.__class__, Formula):
            item = Operand(item)
        return GetItem(self, item)

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


class Operator1(Formula):
    def __init__(self, operator, value):
        super(Operator1, self).__init__()
        self.operator = operator
        self.value = value

    def traverse(self):
        return self.value.traverse() + ["'" + self.operator]

class Operator2(Formula):
    def __init__(self, operator, left, right):
        super(Operator2, self).__init__()
        self.operator = operator
        self.left = left
        self.right = right

    def traverse(self):
        return self.left.traverse() + self.right.traverse() + [self.operator]

class Operand(Formula):
    COUNTER = 0
    def __init__(self, value):
        super(Operand, self).__init__()
        self.value = value

    def traverse(self):
        Operand.COUNTER += 1
        return [("CONST_{}".format(Operand.COUNTER), self.value)]

class MethodCall(Formula):
    def __init__(self,value,  method, args, kwargs):
        super(MethodCall, self).__init__()
        self.value = value
        self.method = method
        self.args = args
        self.kwargs = kwargs

    def traverse(self):
        return (self.value.traverse() +
                reduce(lambda n, x: n + x.traverse(), self.args, [])
                + ["mc__{}".format(len(self.args)) + self.method])

class GetItem(Formula):
    def __init__(self, value, item):
        super(GetItem, self).__init__()
        self.value = value
        self.item = item

    def traverse(self):
        return (self.value.traverse() +
                self.item.traverse() +
                ["__gi__"])

class FunctionCall(Formula):
    COUNTER = 0
    def __init__(self, func, args):
        super(FunctionCall, self).__init__()
        self.func = func
        self.args = args

    def traverse(self):
        return (reduce(lambda n, x: n + x.traverse(), self.args, [])
                + [("BINDFUNC_{}".format(FunctionCall.COUNTER), self.func, len(self.args))])


class Underscore(Formula):
    def __init__(self):
        super(Underscore, self).__init__()
        pass

    def traverse(self):
        return ["___ARG___"]

def scalambdable_func(f):
    @functools.wraps(f)
    def wraps(*args, **kwargs):
        return FunctionCall(f, map(Formula.convert_oprand, args))
    return wraps

_ = Underscore()
SF = scalambdable_func

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
    def test(x):
        return 100 + x
    print (scalambdable_func(test)(10) + _)(1000)
    l = _ + 1
    print map(l, [1, 2, 3, 4])
    print _[1]
