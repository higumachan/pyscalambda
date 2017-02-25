import copy

from pyscalambda.base_formula import BaseFormula

from pyscalambda.utility import convert_operand, is_scalambda_object


class Formula(BaseFormula):
    @property
    def __name__(self):
        return self._get_lambda().__name__

    def __init__(self):
        self.is_cache = True
        self.cache_lambda = None
        self.cache_consts = None
        self.children = []

    def __str__(self):
        return self._create_lambda_string()

    def debug(self):
        return self._create_lambda_string(), list(self._traverse_const_values())

    def nocache(self):
        self.is_cache = False
        return self


    def __call__(self, *args):
        """

        :type args: List of Any
        :rtype: Callable
        """
        return self._get_lambda()(*args)

    def if_(self, cond):
        from pyscalambda.formula_nodes import If
        return If(convert_operand(cond), convert_operand(self))

    def in_(self, iterator):
        from pyscalambda.operators import BinaryOperator
        if not hasattr(iterator, "__iter__"):
            raise TypeError("argument of type '{}' is not iterable".format(type(iterator).__name__))
        return BinaryOperator(" in ", convert_operand(self), convert_operand(iterator))

    def not_in_(self, iterator):
        from pyscalambda.operators import BinaryOperator
        if not hasattr(iterator, "__iter__"):
            raise TypeError("argument of type '{}' is not iterable".format(type(iterator).__name__))
        return BinaryOperator(" not in ", convert_operand(self), convert_operand(iterator))

    def and_(self, other):
        from pyscalambda.operators import BinaryOperator
        if not is_scalambda_object(other):
            raise TypeError("other is only scalambdable object")
        return BinaryOperator("and", self, other)

    def or_(self, other):
        from pyscalambda.operators import BinaryOperator
        if not is_scalambda_object(other):
            raise TypeError("other is only scalambdable object")
        return BinaryOperator("or", self, other)

    def _create_lambda_string(self):
        traversed = list(self._traverse())
        body = "".join(traversed)

        constized_args = sorted(list(set(self._traverse_constize_args())))
        unnamed_args = list(self._traverse_args())
        if len(constized_args) == 0:
            args = ",".join(unnamed_args)
        elif len(unnamed_args) == 0:
            args = ",".join(constized_args)
        else:
            raise SyntaxError("_ and _1 ~ _9 can not be used at the same time. {} {}".
                              format(constized_args, unnamed_args))
        return "lambda {}:{}".format(args, body)

    def _create_lambda(self):
        """

        :return: Callable
        """
        binds = dict(self._traverse_const_values())
        binds['copy'] = copy
        lambda_string = self._create_lambda_string()
        return eval(lambda_string, binds)

    def _get_lambda(self):
        """

        :rtype: Callable
        """
        if not self.is_cache or self.cache_lambda is None:
            self.cache_lambda = self._create_lambda()
        return self.cache_lambda

    def _traverse(self):
        pass

    def _traverse_const_values(self):
        for child in self.children:
            for t in child._traverse_const_values():
                yield t

    def _traverse_args(self):
        for child in self.children:
            for t in child._traverse_args():
                yield t

    def _traverse_constize_args(self):
        for child in self.children:
            for t in child._traverse_constize_args():
                yield t
