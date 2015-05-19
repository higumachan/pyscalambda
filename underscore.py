

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
        return "lambda {}: {}".format(",".join(self.operand), " ".join(sum(map(list, zip(self.operand, self.operator)), []) + [self.operand[-1]]))

    def __call__(self, *args):
        lambda_string = self.create_lambda_string()
        self.operand
        return eval(lambda_string)(*args)

_ = Underscore()

if __name__ == '__main__':
    (lambda x, y, z: x + y + z)(1, 2, 3)
    print (_ * _ * _ * _)(1, 2, 3, 4)

