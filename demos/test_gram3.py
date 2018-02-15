"""
Sample code using version 3 of makogram grammar
"""

from ..makogram.grammar import Grammar, Proc

import logging
logging.basicConfig(format='%(levelname)s:%(message)s',
                        level=logging.DEBUG)
log = logging.getLogger(__name__)

log.debug("Creating grammar object")
g = Grammar()

# This is wrong --- we can subclass Renderable and
# redefine 'render' method, OR we can wrap a function
# in a Proc object, but we don't do both at the same time.
#
#class Noun(Proc):
#    def render(self):
#         return "Dog"

log.debug("Wrapping 'canine' function in Proc object as noun")

# Here is how to wrap 
def canine():
    return "Dog"
dog = Proc(g, canine)
cat = "cat"

# Meow as raw function, we'll do the wrapping in grammar
def meow():
    return "Meow"


log.debug("Production S -> N V")
g.prod("S", "${N()} ${V()}")
log.debug("Production N -> noun")
g.prod("N", dog)
g.prod("N", cat)

log.debug("Production V -> meow")
g.prod("V", meow)

print( g.gen("S") )




