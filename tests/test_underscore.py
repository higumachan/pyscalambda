from functools import reduce
from unittest import TestCase

from nose.tools import (
    eq_,
    raises
)

from pyscalambda import SC, SF, Q, _, _1, _2


class UnderscoreTest(TestCase):
    def test_identity(self):
        eq_(_(1), 1)
        eq_(_(2), 2)
        eq_(_([1, 2]), [1, 2])

    def test_calc_number_operator2(self):
        eq_((_ + _)(1, 1), 2)
        eq_((_ - _)(1, 1), 0)
        eq_((_ * _)(1, 1), 1)
        eq_((_ / _)(1, 1), 1)
        eq_((_ ** _)(1, 1), 1)

    def test_calc_number_left_operator(self):
        eq_((_ + 2)(2), 4)
        eq_((_ - 2)(2), 0)
        eq_((_ * 2)(2), 4)
        eq_((_ / 2)(2), 1)
        eq_((_ ** 2)(2), 4)

    def test_calc_number_right_operator(self):
        eq_((3 + _)(1), 4)
        eq_((3 - _)(1), 2)
        eq_((3 * _)(1), 3)
        eq_((3 / _)(1), 3)
        eq_((3 ** _)(1), 3)

    def test_calc_complex_formula(self):
        eq_((3 + _ * 4 + _)(1, 2), 9)
        eq_((3 + _ * 4 + (_ + 1) * 100)(1, 2), 307)
        eq_((10 + -_ * 2)(1), 8)
        eq_(((10 + -_) * 2)(1), 18)

    def test_call_method(self):
        eq_((_.split(","))("test,nadeko"), ["test", "nadeko"])
        eq_((_.split(",") + ["rikka"])("test,nadeko"), ["test", "nadeko", "rikka"])

    def test_str_args(self):
        eq_((_ + " is " + _)("nadeko", "cute"), "nadeko is cute")
        eq_((_ * _)("nadeko", 4), "nadeko" * 4)

    def test_already_bindings(self):
        x = 1
        eq_((_ + x)(1), 2)

    def test_bug_case1(self):
        eq_(("_a" + _)("test"), "_atest")

    def test_bug_case2(self):
        class A(object):
            def __init__(self, x):
                self.x = x

        class B(object):
            def __init__(self):
                pass

            def f(self, x):
                return A(x)
        a = A(100)
        b = B()
        eq_((_.x)(a), 100)
        eq_((_.f().x)(b), 100)

    def test_scalambdable_func(self):
        def test(x):
            return 100 + x

        def test2(x, y):
            return x + y + 1

        eq_((SF(test)(10) + _)(1000), 1110)
        eq_(SF(len)(_)([1, 2, 3]), 3)
        eq_(SF(len)(_)(list(range(100))), 100)
        eq_((SF(len)(_) + 1)([list(range(1)), list(range(2)), list(range(3))]), 4)
        eq_(list(map((SF(len)(_) + 1), [list(range(1)), list(range(2)), list(range(3))])), [2, 3, 4])
        eq_((SF(test2)(_, 2) + 1)(100), 104)
        eq_(
            list(map(SF(test), list(map((SF(len)(_) + 1), [list(range(1)), list(range(2)), list(range(3))])))),
            [102, 103, 104]
        )
        eq_(SF(test)(10), 110)

    def test_scalambdable_func_multi_args(self):
        eq_(SF(_ + 1, len)(_)([1, 2, 3]), 4)
        eq_(SF(lambda x: x + 1, len)(_)([1, 2, 3]), 4)

        def test(x):
            return x + 1

        eq_(SF(test, len)(_)([1, 2, 3]), 4)

        @SF
        def test2(x):
            return x + 1

        eq_(test2(SF(len)(_))([1, 2, 3]), 4)

    def test_readme(self):
        eq_(list(map(_ + 1, [1, 2, 3, 4])), [2, 3, 4, 5])
        eq_("".join(filter(_.isdigit(), "ab123aad")), "123")
        eq_(reduce(_ + _, [1, 2, 3, 4]), 10)
        eq_(list(map(SF(len)(_) + 1, [[1], [1, 2], [1, 2, 3]])), [2, 3, 4])

    def test_high_stress(self):
        for i in range(6):
            eq_(list(map(_ + 10, range(10 ** i))), list(range(10, 10 ** i + 10)))

    def test_getitem(self):
        eq_(_[0]([1, 2, 3]), 1)
        eq_(_[1]([1, 2, 3]), 2)
        eq_(_[2]([1, 2, 3]), 3)

    def test_member(self):
        class A(object):
            def __init__(self):
                self.a = 100
                self.bc = 10
        a = A()

        assert (_.a(a) == 100)

    def test_1to9_placeholder(self):
        eq_((_1 + _2 * _2)(10, 100), 10010)

    @raises(SyntaxError)
    def test_1to9_placeholder_and_unnamed_placeholder(self):
        eq_((_1 + _2 * _2 + _)(10, 100, 10), 10020)

    def test_not_use_const_dict(self):
        eq_(len((_ + 1 + 1 + 1).debug()[1]), 0)

        class A(object):
            pass

        eq_(len((_ + A()).debug()[1]), 1)

    def test_call_with_kwargs(self):
        class A(object):
            def test(self, test=10):
                return test

        a = A()
        eq_((_.test(test=19))(a), 19)
        eq_((_.test())(a), 10)

        @SF
        def func(x, y=10):
            return x + y

        eq_(func(10, y=_)(100), 110)
        eq_(func(_, y=_)(10, 100), 110)

    def test_scalambdable_const(self):
        eq_(SC(10)(), 10)
        eq_((SC(10) * 10)(), 100)
        
    def test_quote(self):
        eq_(SF(sum, map)(Q(_ + 1), _)([1, 2, 3]), 9)

    def test_virtual_if(self):
        eq_((_2 + 1).if_(_1 < 5).else_(_2 + 2)(0, 10), 11)
        eq_((_2 + 1).if_(_1 < 5).else_(_2 + 2)(10, 10), 12)
        eq_(_.if_(_ < 5).else_(_)(11, 10, 12), 12)
        eq_(_.if_(_ < 5).else_(_)(11, 0, 12), 11)
