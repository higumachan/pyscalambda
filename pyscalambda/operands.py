from pyscalambda.formula import Formula

from pyscalambda.utility import can_str_emmbed, str_emmbed


class Operand(Formula):
    pass


class ConstOperand(Operand):
    COUNTER = 0

    def __init__(self, value):
        super(ConstOperand, self).__init__()
        self.id = ConstOperand.COUNTER
        ConstOperand.COUNTER += 1
        self.value = value

        self.is_use_dict = not can_str_emmbed(self.value)

    def _traverse(self):
        yield '('
        yield "CONST_{}".format(self.id) if self.is_use_dict else str_emmbed(self.value)
        yield ')'

    def _traverse_const_values(self):
        if self.is_use_dict:
            yield ('CONST_{}'.format(self.id), self.value)


class DeepConstOperand(ConstOperand):
    def _traverse(self):
        yield '('
        yield "copy.deepcopy(CONST_{})".format(self.id) if self.is_use_dict else str_emmbed(self.value)
        yield ')'


class UndefinedConstOperand(Operand):

    def __init__(self, value_name):
        super(UndefinedConstOperand, self).__init__()
        self.value_name = value_name

    def _traverse(self):
        yield '('
        yield self.value_name
        yield ')'


class Underscore(Operand):
    NUMBER_CONSTIZE = 10
    COUNTER = NUMBER_CONSTIZE

    def __init__(self, id=None, in_arglist=True):
        super(Underscore, self).__init__()
        if id is None:
            self.id = Underscore.COUNTER
            Underscore.COUNTER += 1
        else:
            self.id = id
        self.in_arglist = in_arglist

    def _traverse(self):
        yield '('
        yield "___ARG{}___".format(self.id)
        yield ')'

    def _traverse_args(self):
        if self.in_arglist and not isinstance(self.id, str) and self.id >= Underscore.NUMBER_CONSTIZE:
            yield "___ARG{}___".format(self.id)

    def _traverse_constize_args(self):
        if self.in_arglist and (isinstance(self.id, str) or self.id < Underscore.NUMBER_CONSTIZE):
            yield "___ARG{}___".format(self.id)

    def is_named(self):
        return self.id == 0 or self.id >= Underscore.NUMBER_CONSTIZE
