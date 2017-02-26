from functools import reduce
from unittest import TestCase
from itertools import product

from nose.tools import (
    assert_is_not,
    eq_,
    ok_,
    raises,
)

from pyscalambda.formula_nodes import Formula

from pyscalambda import not_, Q, SC, SD, SF, SI, _, _1, _2, _3


def not_formula_and_eq(a, b, msg=None):
    if issubclass(a.__class__, Formula):
        raise AssertionError(msg)
    if issubclass(b.__class__, Formula):
        raise AssertionError(msg)
    eq_(a, b, msg)


def not_formula_and_ok(expr, msg=None):
    if issubclass(expr.__class__, Formula):
        raise AssertionError(msg)
    ok_(expr, msg)


class UnderscoreTest(TestCase):
    def test_identity(self):
        not_formula_and_eq(_(1), 1)
        not_formula_and_eq(_(2), 2)
        not_formula_and_eq(_([1, 2]), [1, 2])

    def test_calc_number_operator2(self):
        not_formula_and_eq((_ + _)(1, 1), 2)
        not_formula_and_eq((_ - _)(1, 1), 0)
        not_formula_and_eq((_ * _)(1, 1), 1)
        not_formula_and_eq((_ / _)(1, 1), 1)
        not_formula_and_eq((_ ** _)(1, 1), 1)

    def test_calc_number_left_operator(self):
        not_formula_and_eq((_ + 2)(2), 4)
        not_formula_and_eq((_ - 2)(2), 0)
        not_formula_and_eq((_ * 2)(2), 4)
        not_formula_and_eq((_ / 2)(2), 1)
        not_formula_and_eq((_ ** 2)(2), 4)

    def test_calc_number_right_operator(self):
        not_formula_and_eq((3 + _)(1), 4)
        not_formula_and_eq((3 - _)(1), 2)
        not_formula_and_eq((3 * _)(1), 3)
        not_formula_and_eq((3 / _)(1), 3)
        not_formula_and_eq((3 ** _)(1), 3)

    def test_calc_complex_formula(self):
        not_formula_and_eq((3 + _ * 4 + _)(1, 2), 9)
        not_formula_and_eq((3 + _ * 4 + (_ + 1) * 100)(1, 2), 307)
        not_formula_and_eq((10 + -_ * 2)(1), 8)
        not_formula_and_eq(((10 + -_) * 2)(1), 18)

    def test_call_method(self):
        not_formula_and_eq((_.split(","))("test,nadeko"), ["test", "nadeko"])
        not_formula_and_eq((_.split(",") + ["rikka"])("test,nadeko"), ["test", "nadeko", "rikka"])

    def test_str_args(self):
        not_formula_and_eq((_ + " is " + _)("nadeko", "cute"), "nadeko is cute")
        not_formula_and_eq((_ * _)("nadeko", 4), "nadeko" * 4)

    def test_already_bindings(self):
        x = 1
        not_formula_and_eq((_ + x)(1), 2)

    def test_bug_case1(self):
        not_formula_and_eq(("_a" + _)("test"), "_atest")

    def test_scalambdable_func(self):
        def test(x):
            return 100 + x

        def test2(x, y):
            return x + y + 1

        not_formula_and_eq((SF(test)(10) + _)(1000), 1110)
        not_formula_and_eq(SF(len)(_)([1, 2, 3]), 3)
        not_formula_and_eq(SF(len)(_)(list(range(100))), 100)
        not_formula_and_eq((SF(len)(_) + 1)([list(range(1)), list(range(2)), list(range(3))]), 4)
        not_formula_and_eq(list(map((SF(len)(_) + 1), [list(range(1)), list(range(2)), list(range(3))])), [2, 3, 4])
        not_formula_and_eq((SF(test2)(_, 2) + 1)(100), 104)
        not_formula_and_eq(
            list(map(SF(test), list(map((SF(len)(_) + 1), [list(range(1)), list(range(2)), list(range(3))])))),
            [102, 103, 104]
        )
        not_formula_and_eq(SF(test)(10), 110)

    def test_scalambdable_func_multi_args(self):
        not_formula_and_eq(SF(_ + 1, len)(_)([1, 2, 3]), 4)
        not_formula_and_eq(SF(lambda x: x + 1, len)(_)([1, 2, 3]), 4)

        def test(x):
            return x + 1

        not_formula_and_eq(SF(test, len)(_)([1, 2, 3]), 4)

        @SF
        def test2(x):
            return x + 1

        not_formula_and_eq(test2(SF(len)(_))([1, 2, 3]), 4)

    def test_readme(self):
        not_formula_and_eq(list(map(_ + 1, [1, 2, 3, 4])), [2, 3, 4, 5])
        not_formula_and_eq("".join(filter(_.isdigit(), "ab123aad")), "123")
        not_formula_and_eq(reduce(_ + _, [1, 2, 3, 4]), 10)
        not_formula_and_eq(list(map(SF(len)(_) + 1, [[1], [1, 2], [1, 2, 3]])), [2, 3, 4])

    def test_high_stress(self):
        for i in range(6):
            not_formula_and_eq(list(map(_ + 10, range(10 ** i))), list(range(10, 10 ** i + 10)))

    def test_getitem(self):
        not_formula_and_eq(_[0]([1, 2, 3]), 1)
        not_formula_and_eq(_[1]([1, 2, 3]), 2)
        not_formula_and_eq(_[2]([1, 2, 3]), 3)

    def test_member(self):
        class A(object):
            def __init__(self):
                self.a = 100
                self.bc = 10
        a = A()

        assert (_.a(a) == 100)

    def test_1to9_placeholder(self):
        not_formula_and_eq((_1 + _2 * _2)(10, 100), 10010)

    @raises(SyntaxError)
    def test_1to9_placeholder_and_unnamed_placeholder(self):
        not_formula_and_eq((_1 + _2 * _2 + _)(10, 100, 10), 10020)

    def test_not_use_const_dict(self):
        not_formula_and_eq(len((_ + 1 + 1 + 1).debug()[1]), 0)

        class A(object):
            pass

        not_formula_and_eq(len((_ + A()).debug()[1]), 1)

    def test_call_with_kwargs(self):
        class A(object):
            def test(self, test=10):
                return test

        a = A()
        not_formula_and_eq((_.test(test=19))(a), 19)
        not_formula_and_eq((_.test())(a), 10)

        @SF
        def func(x, y=10):
            return x + y

        not_formula_and_eq(func(10, y=_)(100), 110)
        not_formula_and_eq(func(_, y=_)(10, 100), 110)

    def test_scalambdable_const(self):
        not_formula_and_eq(SC(10)(), 10)
        not_formula_and_eq((SC(10) * 10)(), 100)

    def test_quote(self):
        not_formula_and_eq(SF(sum, map)(Q(_ + 1), _)([1, 2, 3]), 9)

    def test_virtual_if(self):
        not_formula_and_eq((_2 + 1).if_(_1 < 5).else_(_2 + 2)(0, 10), 11)
        not_formula_and_eq((_2 + 1).if_(_1 < 5).else_(_2 + 2)(10, 10), 12)
        not_formula_and_eq(_.if_(_ < 5).else_(_)(11, 10, 12), 12)
        not_formula_and_eq(_.if_(_ < 5).else_(_)(11, 0, 12), 11)

    def test_deep_const(self):
        l = [1, 2, 3]
        assert_is_not(SD(l)(), l)
        (SD(l).append(_))(4)
        not_formula_and_eq(l, [1, 2, 3])

        (SC(l).append(_))(4)
        not_formula_and_eq(l, [1, 2, 3, 4])

    def test_scalambdable_iterator(self):
        not_formula_and_eq(SI([1, 2, 3])(), [1, 2, 3])
        not_formula_and_eq(SI([1, _, 3])(10), [1, 10, 3])
        not_formula_and_eq(SI([_, _, 3])(10, 20), [10, 20, 3])

        not_formula_and_eq(SI((1, 2, 3))(), (1, 2, 3))
        not_formula_and_eq(SI((1, _, 3))(10), (1, 10, 3))
        not_formula_and_eq(SI((_, _, 3))(10, 20), (10, 20, 3))

        not_formula_and_eq(SI({1, 2, _1})(10), {1, 2, 10})

        not_formula_and_eq(SI({"a": 1, "b": 2})(), {"a": 1, "b": 2})
        not_formula_and_eq(SI({"a": _1, "b": 2})(10), {"a": 10, "b": 2})
        not_formula_and_eq(SI({_1: _2, _3: 2})("a", 20, "c"), {"a": 20, "c": 2})

    @raises(SyntaxError)
    def test_scalambda_iterator_dict_syntax_error1(self):
        not_formula_and_eq(SI({_: _, "b": _})("k", 10, 20), {"k": 10, "b": 20}) # because can't decide argument order

    @raises(SyntaxError)
    def test_scalambda_iterator_dict_syntax_error2(self):
        not_formula_and_eq(SI({_: 2, _: 1})("a", "c"), {"a": 2, "c": 1}) # because can't decide argument order

    @raises(SyntaxError)
    def test_scalambda_iterator_set_syntax_error(self):
        not_formula_and_eq(SI({1, 2, _})(10), {1, 2, 10}) # because can't decide argument order

    def test_virtual_in(self):
        for iter_class in [set, list, tuple]:
            not_formula_and_ok(SC(1).in_(_)(iter_class([1, 2, 3])))
            not_formula_and_ok(not SC(4).in_(_)(iter_class([1, 2, 3])))
            not_formula_and_ok(_.in_(_)(2, iter_class([1, 2, 3])))

    @raises(TypeError)
    def test_virtual_in_type_error(self):
        _.in_(12)(100)

    def test_virtual_not_in(self):
        for iter_class in [set, list, tuple]:
            not_formula_and_ok(not SC(1).not_in_(_)(iter_class([1, 2, 3])))
            not_formula_and_ok(SC(4).not_in_(_)(iter_class([1, 2, 3])))
            not_formula_and_ok(not _.not_in_(_)(2, iter_class([1, 2, 3])))

    @raises(TypeError)
    def test_virtual_not_in_type_error(self):
        _.not_in_(12)(100)

    def test_virtual_logic_and(self):
        for x, y in product([True, False], [True, False]):
            not_formula_and_eq(_.and_(SC(x))(y), x and y)
            not_formula_and_eq(SC(x).and_(_)(y), x and y)

    @raises(TypeError)
    def test_virtual_logic_and_not_callable(self):
        not_formula_and_eq(_.and_(True)(False), None)

    def test_virtual_logic_or(self):
        for x, y in product([True, False], [True, False]):
            not_formula_and_eq(_.or_(SC(x))(y), x or y)
            not_formula_and_eq(SC(x).or_(_)(y), x or y)

    @raises(TypeError)
    def test_virtual_logic_or_not_callable(self):
        not_formula_and_eq(_.or_(True)(False), None)

    def test_virtual_not(self):
        not_formula_and_ok(not not_(_)(True))
        not_formula_and_ok(not_(_)(False))
        not_formula_and_ok(not_(_.and_(SC(False)))(False))
        not_formula_and_ok(not_(_.and_(SC(False)))(True))
        not_formula_and_ok(not not_(_.and_(SC(True)))(True))
        not_formula_and_ok(not_(_.or_(SC(False)))(False))
        not_formula_and_ok(not not_(_.or_(SC(False)))(True))
        not_formula_and_ok(not not_(_.or_(SC(True)))(True))

    def test_get_attribute(self):
        class A(object):
            def __init__(self, x):
                self.x = x

        a = A(10)
        not_formula_and_eq(_.x.M(a), 10)
        not_formula_and_eq((_.x + 1)(a), 11)
