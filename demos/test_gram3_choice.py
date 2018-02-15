"""
Sample code using version 3 of makogram grammar
"""
import context
from makogram.grammar import Grammar, Proc

import logging
logging.basicConfig(format='%(levelname)s:%(message)s',
                        level=logging.DEBUG)
log = logging.getLogger(__name__)

log.debug("Creating grammar object")
g = Grammar()

g.prod("S", "dog")
g.prod("S", "cat")

print("Dumping grammar")
print(g)

s = g.gen("S")
print(s)





