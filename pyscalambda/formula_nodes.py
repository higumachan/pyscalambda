from pyscalambda.formula import Formula
from pyscalambda.utility import convert_operand


class MethodCall(Formula):
    def __init__(self, value, method, args, kwargs):
        super(MethodCall, self).__init__()
        self.value = value
        self.method = method
        self.args = args
        self.kwargs = kwargs
        self.children = [self.value] + self.args + list(self.kwargs.values())

    def traverse(self):
        yield '('
        for t in self.value.traverse():
            yield t
        yield '.'
        yield self.method
        yield '('
        for arg in self.args:
            for t in arg.traverse():
                yield t
            yield ','
        for name, arg in self.kwargs.items():
            yield '{}='.format(name)
            for t in arg.traverse():
                yield t
            yield ','
        yield ')'
        yield ')'


class GetItem(Formula):
    def __init__(self, value, item):
        super(GetItem, self).__init__()
        self.value = value
        self.item = item
        self.children = [self.value, self.item]

    def traverse(self):
        yield '('
        for t in self.value.traverse():
            yield t
        yield '['
        for t in self.item.traverse():
            yield t
        yield ']'
        yield ')'


class FunctionCall(Formula):
    COUNTER = 0

    def __init__(self, func, args, kwargs):
        super(FunctionCall, self).__init__()
        self.id = FunctionCall.COUNTER
        FunctionCall.COUNTER += 1
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.children = self.args + list(self.kwargs.values())

    def traverse(self):
        yield "BIND_FUNC_{}".format(self.id)
        yield '('
        for arg in self.args:
            for t in arg.traverse():
                yield t
            yield ','
        for name, arg in self.kwargs.items():
            yield '{}='.format(name)
            for t in arg.traverse():
                yield t
            yield ','
        yield ')'

    def traverse_const_values(self):
        yield ('BIND_FUNC_{}'.format(self.id), self.func)
        for t in super(FunctionCall, self).traverse_const_values():
            yield t


class Quote(Formula):
    COUNTER = 0

    def __init__(self, formula):
        super(Quote, self).__init__()
        self.id = Quote.COUNTER
        self.formula = formula
        self.children = []
        Quote.COUNTER += 1

    def __call__(self, *args, **kwargs):
        kwargs = dict(map(lambda x: (x[0], convert_operand(x[1])), kwargs.items()))
        return self.formula(*map(convert_operand, args), **kwargs)

    def traverse(self):
        yield '('
        yield 'INNER_LAMBDA_{}'.format(self.id)
        yield ')'

    def traverse_const_values(self):
        for const_value in self.formula.traverse_const_values():
            yield const_value
        from pyscalambda.scalambdable import scalambdable_func
        yield (
            'INNER_LAMBDA_{}'.format(self.id),
            scalambdable_func(self.formula.get_lambda())
        )


class IfElse(Formula):
    def __init__(self, cond, true, false):
        super(IfElse, self).__init__()
        self.children = [true, cond, false]
        self.cond = cond
        self.true = true
        self.false = false

    def traverse(self):
        yield '('
        for t in self.true.traverse():
            yield t
        yield ' if '
        for t in self.cond.traverse():
            yield t
        yield 'else '
        for t in self.false.traverse():
            yield t
        yield ')'


class If(Formula):
    def __init__(self, cond, true):
        super(If, self).__init__()
        self.children = [true, cond]
        self.cond = cond
        self.true = true

    def else_(self, false):
        return IfElse(self.cond, self.true, convert_operand(false))

    def traverse(self):
        yield '('
        for t in self.true.traverse():
            yield t
        yield ' if '
        for t in self.cond.traverse():
            yield t
        yield 'else '
        yield 'None'
        yield ')'


class MakeIterator(Formula):
    def __init__(self, iter, opener, closer):
        super(MakeIterator, self).__init__()
        self.iter = list(iter)
        self.type = type
        self.children = self.iter
        self.opener = opener
        self.closer = closer

    def traverse(self):
        yield self.opener
        for item in self.iter:
            for t in item.traverse():
                yield t
            yield ','
        yield self.closer


class MakeDictionary(Formula):
    def __init__(self, keys, values):
        super(MakeDictionary, self).__init__()
        self.keys = list(keys)
        self.values = list(values)
        self.type = type
        self.children = self.keys + self.values

    def traverse(self):
        yield '{'
        for k, v in zip(self.keys, self.values):
            for t in k.traverse():
                yield t
            yield ':'
            for t in v.traverse():
                yield t
            yield ','
        yield '}'
