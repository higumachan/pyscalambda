from pyscalambda.formula import Formula


class Operator(Formula):
    pass


class UnaryOperator(Operator):
    def __init__(self, operator, value):
        super(UnaryOperator, self).__init__()
        self.operator = operator
        self.value = value
        self.children = [self.value]

    def _traverse(self):
        yield '('
        yield self.operator
        for t in self.value._traverse():
            yield t
        yield ')'


class BinaryOperator(Operator):
    def __init__(self, operator, left, right):
        '''

        :type operator: str
        :type left: Formula
        :type right: Formula
        '''
        super(BinaryOperator, self).__init__()
        self.operator = operator
        self.left = left
        self.right = right
        self.children = [self.left, self.right]

    def _traverse(self):
        yield '('
        for t in self.left._traverse():
            yield t
        yield self.operator
        for t in self.right._traverse():
            yield t
        yield ')'
