#PyScaLambda

##概要
Scalaの
	
	(_ + _)(1, 2)
	
みたいな感じのラムダ式を書くためのライブラリ

##使い方

	from pyscalambda import _
	
	map(_ + 1, [1, 2, 3, 4]) #== map(lambda x: x + 1, [1, 2, 3, 4]) == [2, 3, 4, 5]
	filter(_.isdigit(), "ab123aad") #==  filter(lambda x: x.isdigit(), "aabb123cc") == "123"
	reduce(_ + _, [1, 2, 3, 4]) # reduce(lambda x, y: x + y, [1, 2, 3, 4]) == 10

## more detail use

_以外にもSFという、関数をラッピングする関数を用意しています。
_を引数に含むような関数呼び出しを行う場合は、呼び出したい関数をSFでラップしてください。

	from pyscalambda import _, SF
	
	map(SF(len(_)) + 1, [[1], [1, 2], [1, 2, 3]])# == map(lambda x: len(x) + 1, [[1], [1, 2], [1, 2, 3]]) == [2, 3, 4]

