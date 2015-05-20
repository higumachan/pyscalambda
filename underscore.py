
OPERATORS = ["+", "-", "*", "/",
        "%", "<", "<=", ">", ">=",
        "==", "!=", "**"]

def parse(l):
    stack = []
    for t in filter(lambda x: not x.isspace(), l):
        if t not in OPERATORS:
            stack.append(t)
        else:
            a = stack.pop()
            b = stack.pop()
            stack.append("({}{}{})".format(b, t, a))
    return stack[0]

class Underscore(object):
    def __init__(self, left=None, right=None, operator=None, operand=None):
        self.left = left
        self.right = right
        self.operand = operand
        self._is_leaf = not left and not right
        self.operator = operator
        self._lambda_cache = None

    def __add__(self, other):
        return self.do(other, "+")

    def __sub__(self, other):
        return self.do(other, "-")

    def __mul__(self, other):
        return self.do(other, "*")

    def __floordiv__(self, other):
        return self.do(other, "/")

    def __mod__(self, other):
        return self.do(other, "%")
    
    def __lt__(self, other):
        return self.do(other, "<")

    def __le__(self, other):
        return self.do(other, "<=")

    def __gt__(self, other):
        return self.do(other, ">")

    def __ge__(self, other):
        return self.do(other, ">=")

    def __eq__(self, other):
        return self.do(other, "==")

    def __ne__(self, other):
        return self.do(other, "!=")

    def __pow__(self, other):
        return self.do(other, "**")

    def __lshift__(self, other):
        return self.do(other, "<<")

    def __rshift__(self, other):
        return self.do(other, ">>")

    def __and__(self, other):
        return self.do(other, "and")

    def __or__(self, other):
        return self.do(other, "or")

    def __xor__(self, other):
        return self.do(other, "xor")

    def __radd__(self, other):
        return self.rdo(other, "+")

    def __rsub__(self, other):
        return self.rdo(other, "-")

    def __rmul__(self, other):
        return self.rdo(other, "*")

    def __rfloordiv__(self, other):
        return self.rdo(other, "/")

    def __rmod__(self, other):
        return self.rdo(other, "%")
    
    def __rlt__(self, other):
        return self.rdo(other, "<")

    def __rle__(self, other):
        return self.rdo(other, "<=")

    def __rgt__(self, other):
        return self.rdo(other, ">")

    def __rge__(self, other):
        return self.rdo(other, ">=")

    def __req__(self, other):
        return self.rdo(other, "==")

    def __rne__(self, other):
        return self.rdo(other, "!=")

    def __rpow__(self, other):
        return self.rdo(other, "**")

    def __rlshift__(self, other):
        return self.rdo(other, "<<")

    def __rrshift__(self, other):
        return self.rdo(other, ">>")

    def __rand__(self, other):
        return self.rdo(other, "and")

    def __ror__(self, other):
        return self.rdo(other, "or")

    def __rxor__(self, other):
        return self.rdo(other, "xor")

    def do(self, other, operator):
        if not isinstance(other, Underscore):
            other = Underscore(operand=other)
        return Underscore(self, other, operator)

    def rdo(self, other, operator):
        if not isinstance(other, Underscore):
            other = Underscore(operand=other)
        return Underscore(other, self, operator)

    def traverse(self):
        if self._is_leaf:
            return ["_"] if self.operand is None else [str(self.operand)]
        return self.left.traverse() + self.right.traverse() + [self.operator]

    def create_lambda_string(self):
        c = [0]
        def us2args(x):
            if x == "_":
                k = c[0]
                c[0] += 1
                return "x{}".format(k)
            return x
        rp_form = map(us2args, self.traverse())
        body =  parse(rp_form)
        args = ",".join(filter(lambda x: x[0] == "x", rp_form))

        return "lambda {}:{}".format(args, body)

    def __str__(self):
        #return " ".join(self.create_lambda_string())
        return self.create_lambda_string()

    def __call__(self, *args):
        if self._lambda_cache is None:
            self._lambda_cache = eval(self.create_lambda_string())
        return self._lambda_cache(*args)

_ = Underscore()

if __name__ == '__main__':
    print (1 + _)(10)
    l = (_ + _)
    print l(1, 2)
    print (_ + _)(1, 2)
    print (_ > ((_ + _) * (_ + _)))(1, 2, 3, 4, 5) 
    print map(_ + 1, [1, 2, 3, 4])

