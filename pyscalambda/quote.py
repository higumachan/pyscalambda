import functools

from pyscalambda.formula import Formula

from pyscalambda.formula_nodes import Quote

from pyscalambda.utility import convert_operand, vmap


def quote(formula):
    return Quote(convert_operand(formula))
