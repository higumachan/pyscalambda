from formula import Formula

from utility import can_str_emmbed, str_emmbed


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

    def traverse(self):
        yield '('
        yield "CONST_{}".format(self.id) if self.is_use_dict else str_emmbed(self.value)
        yield ')'

    def traverse_const_values(self):
        if self.is_use_dict:
            yield ('CONST_{}'.format(self.id), self.value)


class Underscore(Operand):
    NUMBER_CONSTIZE = 10
    COUNTER = NUMBER_CONSTIZE

    def __init__(self, id=None):
        super(Underscore, self).__init__()
        if id is None:
            self.id = Underscore.COUNTER
            Underscore.COUNTER += 1
        else:
            self.id = id

    def traverse(self):
        yield '('
        yield "___ARG{}___".format(self.id)
        yield ')'

    def traverse_args(self):
        if self.id >= Underscore.NUMBER_CONSTIZE:
            yield "___ARG{}___".format(self.id)

    def traverse_constize_args(self):
        if self.id < Underscore.NUMBER_CONSTIZE:
            yield "___ARG{}___".format(self.id)