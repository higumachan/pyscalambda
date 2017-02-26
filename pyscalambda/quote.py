from pyscalambda.formula_nodes import Quote

from pyscalambda.formula import Formula

from pyscalambda.utility import convert_operand


def quote(formula):
    '''

    :type formula: Formula
    :rtype: Quote
    '''
    return Quote(convert_operand(formula))
