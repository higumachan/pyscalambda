#PyScaLambda

## Status
[![CircleCI](https://circleci.com/gh/higumachan/pyscalambda.svg?style=svg)](https://circleci.com/gh/higumachan/pyscalambda)

## Description
Scalaの
```scala
(_ + _)(1, 2)
```
みたいな感じのラムダ式を書くためのライブラリ

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

## more detail use

### scalambdable_function
_以外にもSFという、関数をラッピングする関数を用意しています。
_を引数に含むような関数呼び出しを行う場合は、呼び出したい関数をSFでラップしてください。

```py
from pyscalambda import _, SF
	
map(SF(len)(_) + 1, [[1], [1, 2], [1, 2, 3]]) #== map(lambda x: len(x) + 1, [[1], [1, 2], [1, 2, 3]]) == [2, 3, 4]
```

### 複数回使用する引数
lambda式の中で複数回参照する引数は_1 ~ _9と言うものを用意してあります。
_1 ~ _9は出現の順序ではなく1~9の数字で引数の順番が変わります。
```py
from pyscalambda import _1, _2

(_1 * _1 + _2 * _1)(10, 20) # == 10 * 10 + 20 * 10 == 300
(_2 * _2 + _1 * _2)(10, 20) # == 20 * 20 + 10 * 20 == 600
```
