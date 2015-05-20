from unittest import TestCase
from nose.tools import ok_, eq_
from underscore import _

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

    def test_bug_case1(self):
        eq_(("_a" + _)("test"), "_atest")
