from pyscalambda.formula import Formula


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
        for name, arg in self.kwargs:
            yield '{}='.format(name)
            for t in self.arg.traverse():
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
        for name, arg in self.kwargs:
            yield '{}='.format(name)
            for t in arg.traverse():
                yield t
            yield ','
        yield ')'

    def traverse_const_values(self):
        yield ('BIND_FUNC_{}'.format(self.id), self.func)
        for t in super(FunctionCall, self).traverse_const_values():
            yield t
