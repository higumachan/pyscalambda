#PyScaLambda

##概要
Scalaの
	
	(_ + _)(1, 2)
	
みたいな感じのラムダ式を書くためのライブラリ

##使い方

	from pyscalambda import _
	
	map(_ + 1, [1, 2, 3, 4]) #== [2, 3, 4, 5]
	reduce(_ + _, [1, 2, 3, 4]) #== 10


