from pyscalambda.base_formula import BaseFormula
from pyscalambda.utility import convert_operand


class Formula(BaseFormula):
    @property
    def __name__(self):
        return self.get_lambda().__name__

    def __init__(self):
        self.is_cache = True
        self.cache_lambda = None
        self.cache_consts = None
        self.children = []

    def __str__(self):
        return self.create_lambda_string()

    def debug(self):
        return (self.create_lambda_string(), list(self.traverse_const_values()))

    def nocache(self):
        self.is_cache = False
        return self

    def create_lambda_string(self):
        traversed = list(self.traverse())
        body = "".join(traversed)

        constized_args = sorted(list(set(self.traverse_constize_args())))
        unnamed_args = list(self.traverse_args())
        if len(constized_args) == 0:
            args = ",".join(unnamed_args)
        elif len(unnamed_args) == 0:
            args = ",".join(constized_args)
        else:
            raise SyntaxError("_ and _1 ~ _9 can not be used at the same time. {} {}".
                              format(constized_args, unnamed_args))
        return "lambda {}:{}".format(args, body)

    def create_lambda(self):
        binds = self.traverse_const_values()
        lambda_string = self.create_lambda_string()
        return eval(lambda_string, dict(binds))

    def get_lambda(self):
        if not self.is_cache or self.cache_lambda is None:
            self.cache_lambda = self.create_lambda()
        return self.cache_lambda

    def __call__(self, *args):
        return self.get_lambda()(*args)

    def if_(self, cond):
        from pyscalambda.formula_nodes import If
        return If(convert_operand(cond), convert_operand(self))

    def traverse_const_values(self):
        for child in self.children:
            for t in child.traverse_const_values():
                yield t

    def traverse_args(self):
        for child in self.children:
            for t in child.traverse_args():
                yield t

    def traverse_constize_args(self):
        for child in self.children:
            for t in child.traverse_constize_args():
                yield t
