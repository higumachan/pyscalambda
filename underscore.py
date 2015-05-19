
OPERATORS = ["+", "-", "*", "/",
        "%", "<", "<=", ">", ">=",
        "==", "!="]

def parse(l):
    stack = []
    print l
    for t in filter(lambda x: not x.isspace(), l):
        if t not in OPERATORS:
            stack.append(t)
        else:
            a = stack.pop()
            b = stack.pop()
            stack.append("({}{}{})".format(b, t, a))
        print stack
    return stack[0]

class Underscore(object):
    def __init__(self, left=None, right=None, operator=None, operand=None):
        self.left = left
        self.right = right
        self.operand = operand
        self._is_leaf = not left and not right
        self.operator = operator

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

    def do(self, other, operator):
        if not isinstance(other, Underscore):
            other = Underscore(operand=other)
        return Underscore(self, other, operator)

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
        return eval(self.create_lambda_string())(*args)

_ = Underscore()

if __name__ == '__main__':
    print (_ + _)(1, 2)
    print (_ > ((_ + _) * (_ + _)))(1, 2, 3, 4, 5) 
    print map(_ + 1, [1, 2, 3, 4])

