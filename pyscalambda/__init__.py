from pyscalambda.operands import Underscore

from pyscalambda.quote import quote

from pyscalambda.scalambdable import scalambdable_const, scalambdable_func, scalambdable_iterator

_ = Underscore(0)
_1 = Underscore(1)
_2 = Underscore(2)
_3 = Underscore(3)
_4 = Underscore(4)
_5 = Underscore(5)
_6 = Underscore(6)
_7 = Underscore(7)
_8 = Underscore(8)
_9 = Underscore(9)
SF = scalambdable_func
SC = scalambdable_const
SI = scalambdable_iterator
Q = quote

__all__ = ("_", "_1", "_2", "_3", "_4", "_5", "_6", "_7", "_8", "_9", "SF", "SC", "Q")
