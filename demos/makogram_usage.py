"""
A tiny example of several constructs to include in 
the header comment for makogram.grammar.
"""

import random
import context
from makogram import grammar

g = grammar.Grammar()

# Production rules can be defined from a symbol
# like "NP" and a template using Mako syntax.  In a
# template, a non-terminal like NP would be invoked as ${NP()}
# Direct and indirect recursion is permitted. 
g.prod("Sentence", "The ${NP()}  ${VP()}")
g.prod("NP", "${Adjectives()} ${Noun()}")

# Repetition can be fixed with the reps keyword or
# selected randomly between a min and max bound
g.prod("Adjectives", "${Adj()}", min=0, max=3)

# Functions that return text can also be used as
# definitions of non-terminals
def noun():
    return random.choice(["dog", "cat"])
g.prod("Noun", noun)

def adj():
    return random.choice(["big ", "small "])
g.prod("Adj", adj)

# If multiple productions are given for the same
# non-terminal, it will be treated as a random choice,
# which may be limited and weighted.  
g.prod("VP", "chases mice", weight=3, max_uses=2)
g.prod("VP", "eats ${food()}", weight=1)

g.prod("food", "kibble", weight=2)
g.prod("food", "table scraps")
g.prod("food", "bugs")

# The max-uses holds across any number of calls to
# expand a term in the grammar.  "chases mice" will
# appear at most twice in the following sequence.
print("A top level generation: {}".format(g.gen("Sentence")))
print("A Noun particle generation: {}".format(g.gen("NP")))
print("a verb object generation: {}".format(g.gen("food")))

# Example output:
# The small small small  cat  chases mice
# The big  dog  eats kibble
# The big  dog  chases mice
# The small big  cat  chases mice
# The  cat  eats table scraps
