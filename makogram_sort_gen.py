"""
Generate test cases for the 
built-in Python function 'sorted', 
as an example of grammar-based 
test generation with an oracle built into the 
test driver. 
"""
from makogram.grammar import Grammar
import genseq

g = Grammar()


g.prod("skel", """
import nose

def ordered(s):
    print("Checking order of {}".format("".join(s)))
    if len(s) < 1:
        return True
    prior = s[0]
    for ch in s[1:]:
        if ch < prior:
            return False
        prior = ch
    return True

${tests()}
""")

# tests ::=  tests test | test
#   with weights and limits to always produce
#   
g.prod("tests", "${tests()} ${test()}", max_uses=10)
g.prod("tests", "${test()}", weight=0)

# test ::= (boilerplate with next_name) 
g.prod("test", """
input_str = "${next_name()}"
output_str = sorted(input_str)
print("Sorted {} and got {}".format(input_str, output_str))
assert len(input_str) == len(output_str)
assert ordered(output_str)
""")

#  next_name is a procedural attachment that 
#  draws names from a fixed sequence
# 
names = genseq.names()
@g.procdef("next_name")
def next_name():
    return next(names)

print(g.gen("${skel()}"))


