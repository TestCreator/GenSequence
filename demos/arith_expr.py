"""
Arithmetic expressions grammar. 

This version of the grammar uses a different non-terminal for 
each level of precedence. 
"""

import random
import context
from makogram.grammar import Grammar

g = Grammar()
g.prod("Exp", "${Exp()} ${AddOp()} ${Term()}", max_uses=4, weight=2)
g.prod("Exp", "${Term()}")
g.prod("Term", "${Term()}${MulOp()}${Factor()}", max_uses=4, weight=2)
g.prod("Term", "${Factor()}")
g.prod("Factor", "(${Exp()})", max_uses=4)
g.prod("Factor", "${Var()}", weight=2)

g.prod("AddOp", (lambda : random.choice(["+", "-"])))
g.prod("MulOp", (lambda : random.choice(["*", "/"])))
g.prod("Var", (lambda : random.choice([ "x", "y", "z" ])))

print(g.gen("Exp"))
