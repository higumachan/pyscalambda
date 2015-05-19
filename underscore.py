
"""

class Underscore(object):
    def __init__(self):
        self.operator = []
        self.operand = []
    
    def add_operand(self, other):
        if len(self.operand) == 0:
            self.operand.append("x0")

        if isinstance(other, Underscore):
            self.operand.append("x{}".format(len(self.operand)))
        else:
            self.operand.append(str(other))

    def do(self, other, op):
        self.add_operand(other)
        self.operator.append(op)
        return self

    def __str__(self):
        return self.create_lambda_string()

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

    def __getattr__(self, name):
        return self

    def create_lambda_string(self):
        print self.operand
        print self.operator
        print sum(map(list, zip(self.operand, self.operator)), []) + [self.operand[-1]]
        return "lambda {}: {}{}".format(",".join(self.operand), "(" * len(self.operand)," ".join(sum(map(list, zip(map(lambda x: x + ")", self.operand), self.operator)), []) + [self.operand[-1] + ")"]))

    def __call__(self, *args):
        lambda_string = self.create_lambda_string()
        self.operand
        return eval(lambda_string)(*args)

"""

def parse(l):
    stack = []
    print l
    for t in filter(lambda x: not x.isspace(), l):
        if t[0] == "x":
            stack.append(t)
        else:
            a = stack.pop()
            b = stack.pop()
            stack.append("({}{}{})".format(b, t, a))
        print stack
    return stack[0]

class Underscore(object):
    def __init__(self, left=None, right=None, operator=None):
        self.left = left
        self.right = right
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
        return Underscore(self, other, operator)

    def traverse(self):
        if self._is_leaf:
            return ["_"]
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

