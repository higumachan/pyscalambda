from pyscalambda.formula_nodes import Quote

from pyscalambda.utility import convert_operand


def quote(formula):
    return Quote(convert_operand(formula))
