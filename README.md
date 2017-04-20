# PyScaLambda

## Status
[![CircleCI](https://circleci.com/gh/higumachan/pyscalambda.svg?style=svg)](https://circleci.com/gh/higumachan/pyscalambda)

## Description
This is a library for writing scala like lambda formulas in python
e.g.

```scala
(_ + _)(1, 2)
```

## How to use

### Install
```bash
pip install pyscalambda
```

### Usage
```py
from pyscalambda import _
	
map(_ + 1, [1, 2, 3, 4]) #== map(lambda x: x + 1, [1, 2, 3, 4]) == [2, 3, 4, 5]
filter(_.isdigit(), "ab123aad") #==  filter(lambda x: x.isdigit(), "aabb123cc") == "123"
reduce(_ + _, [1, 2, 3, 4]) #== reduce(lambda x, y: x + y, [1, 2, 3, 4]) == 10
```

## Use Details


### Multi access variable

If a variable is used multiple times in a lambda formula, use _1 to _9 to reduce syntax.

```py
from pyscalambda import _1, _2

(_1 * _1 + _2 * _1)(10, 20) # ==  (lambda x, y: x * x + y * x)(10, 20) ==  300
(_2 * _2 + _1 * _2)(10, 20) # == (lambda x, y: y * y + x * y)(10, 20) == 600
```

#### Caution

* Don't use _ and _1 to _9 in same time. *

```py
(_ + _1)(1, 2) # raising SyntaxError
```

### Scalambdable_function (SF)
To convert to pyscalambda for this example code.
```py
map(lambda x: len(x) + 1,  [[1], [1, 2], [1, 2, 3]])
```

But _ can't hook function caller.
Scalambdable function solve such cases

e.g.

```py
from pyscalambda import _, SF # SF is scalambdable function's alias

map(SF(len)(_) + 1, [[1], [1, 2], [1, 2, 3]]) #== map(lambda x: len(x) + 1, [[1], [1, 2], [, 2, 3]]) == [2, 3, 4]
```

SF can also be used as a decorator when user define function case  

e.g.

```py
from pyscalambda import _, SF # SF is scalambdable function's alias

@SF
def func(x):
    return x + 1


map(func(_) * 2, [1, 2, 3]) #== map(lambda x: func(x) + 1, [1, 2, 3]) == [4, 6, 8]
```

If you use nesting SF, you can refactor to SF multi arguments. (composition of functions)  

e.g.

```py
from pyscalambda import _, SF

def func(x):
    return x ** x

map(SF(func)(SF(len))(_), [1, 2, 3]))
```

Above code can be replaces as:

```py
from pyscalambda import _, SF

def func(x):
    return x ** x

map(SF(func, len))(_), [1, 2, 3]))
```

### Scalambdable_iterator (SI)

Following code can be converted to pyscalambda api as :

```py
map(lambda x: (x[0] + 1, x[1] + 20),  [(1, 2), (3, 4)])
map(lambda x: ({"x + 1": x + 1, "x + 2": x + 2),  [1, 2])
```

But _ can't hook contruction iterator.  
Scalambdable iterator can solve this.

```py
from pyscalambda import _, _1, SI # SI is scalambdable iterators's alias

map(SI((_[0] + 1, _[1] + 2)),  [(1, 2), (3, 4)])
map(SI({"x + 1": _1 + 1, "x + 2": _1 + 2),  [1, 2]) # this case can't use _. because can't deceide argument order.
```

### Quote (Q)

Quote is in order to realize "lambda in lambda" on pyscalambda.

Example:
```py
map(lambda x: reduce(lambda y, z: y ** z, x),  [[1, 2], [3, 4]])
```

By directly replacing.

```py
# WARING: This program is wrong
from pyscalambda import _

map(SF(reduce)(_ ** _, _), [[1, 2], [3, 4])
```

This program convert to 

```py
map(lambda x, y, z: reduce(y ** z, x),  [[1, 2], [3, 4]])
```

Because replace _ dosen't have hierarchy (like indent)

Quote solve this.

```py
from pyscalambda import _, Q

map(SF(reduce)(Q(_ ** _), _), [[1, 2], [3, 4])
```

This program is correct to replace.

### Virtual if

"Virtual if" is a "move like a ternary conditional operator" methods.

If you want to replace to pyscalambda this code.

```py
map(lambda x: x if x == 0 else -1, [1, 2, 0, 4])
```

But _ can't hook ternary conditional operator

"Virtual if" feature can be solve such a case

```py
from pyscalambda import _

map(_.if_(_ == x).else_(-1), [1, 2, None, 4])
```


