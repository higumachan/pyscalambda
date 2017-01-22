from pyscalambda.formula import Formula


class Operator(Formula):
    pass


class UnaryOperator(Operator):
    def __init__(self, operator, value):
        super(UnaryOperator, self).__init__()
        self.operator = operator
        self.value = value
        self.children = [self.value]

    def traverse(self):
        yield '('
        yield self.operator
        for t in self.value.traverse():
            yield t
        yield ')'


class BinaryOperator(Operator):
    def __init__(self, operator, left, right):
        super(BinaryOperator, self).__init__()
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
