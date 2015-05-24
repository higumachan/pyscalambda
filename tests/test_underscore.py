from unittest import TestCase
from nose.tools import ok_, eq_
from pyscalambda import _, SF

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

    def test_scalambdable_func(self):
        def test(x):
            return 100 + x
        def test2(x, y):
            return x + y + 1
        eq_((SF(test)(10) + _)(1000), 1110)
        eq_(SF(len)(_)([1, 2, 3]), 3)
        eq_(SF(len)(_)(range(100)), 100)
        eq_((SF(len)(_) + 1)([range(1), range(2), range(3)]), 4)
        eq_(map((SF(len)(_) + 1), [range(1), range(2), range(3)]), [2, 3, 4])
        eq_((SF(test2)(_, 2) + 1)(100), 104)

    def test_readme(self):
        eq_(map(_ + 1, [1, 2, 3, 4]), [2, 3, 4, 5])
        eq_(filter(_.isdigit(), "ab123aad"), "123")
        eq_(reduce(_ + _, [1, 2, 3, 4]), 10)
        eq_(map(SF(len)(_) + 1, [[1], [1, 2], [1, 2, 3]]), [2, 3, 4])
    
    def test_high_stress(self):
        for i in range(6):
            eq_(map(_ + 10, xrange(10 ** i)), range(10, 10 ** i + 10))
