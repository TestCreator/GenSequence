"""
Simple test of generating sentences with makogram grammar, 
reworked for the new version

Tests the Choice, Proc, and Template subclasses of 
renderable; does not test Kleene  (not yet implemented). 
Does not test weights and limits in expansion of choices. 

Run as 'python3 tests/makogram_test.py' will show info messages; 
run as 'nosetests tests/makogram_test.py' will suppress messages 
unless the test fails. 
"""

import logging
logging.basicConfig(format='%(levelname)s:%(message)s',
                        level=logging.INFO)
log = logging.getLogger(__name__)

## Ridiculous path hack so that this can work both within and
## outside of nosetests, locally and from the main project folder.
## 
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from makogram.grammar import Grammar

import random
import re  # For the oracle


# Attempt to simulate a generative grammar for
#   Expr ::=  small_int
#   Expr ::=  Expr + Expr
#
#   We define the symbols in two different ways: 
#   1.  We define Expr using grammar rules. 
#   2.  We define small_int procedurally so that we
#       can use the Python random library within it.
#



g = Grammar()
g.prod("sentence", "${article()} ${noun_phrase()} ${intransitive()}")
g.prod("sentence", "${article()} ${noun_phrase()} ${transitive()} ${article()} ${noun_phrase()}")

g.prod("noun_phrase", "${adjective()} ${noun_phrase()}")
g.prod("noun_phrase", "${noun()}")

def article():
    return random.choice(["the", "a"])
g.prod("article", article)

def noun():
    return random.choice(["ball", "man", "house", "squirrel"])
g.prod("noun", noun)

def adjective():
    return random.choice(["big", "green", "brown", "scary"])
g.prod("adjective", adjective)

def intransitive():
    return random.choice(["eats", "sleeps", "falls down"])
g.prod("intransitive", intransitive)

def transitive():
    return random.choice(["eats", "builds", "hits", "likes", "throws"])
g.prod("transitive", transitive)

log.debug("*** Grammar ***")
log.debug(g)
log.debug("*** Expanding sentence ***")



# Here is the pattern we're trying to match (for the oracle)
pat = re.compile(r"""(the|a)\s
                     ((big|green|brown|scary)\s)*
                     (ball|man|house|squirrel)\s 
                     ( (eats|sleeps|falls.down)
                     | (eats|builds|hits|likes|throws)\s 
                       (the|a)\s
                       ((big|green|brown|scary)\s)* 
                       (ball|man|house|squirrel)  )
                  """, re.VERBOSE)


def test_generated_sentences():
    for _ in range(20): 
        sentence = g.gen("sentence")
        log.info("Generated sentence: {}".format(sentence))
        assert pat.fullmatch(sentence)

if __name__ == "__main__":
    test_generated_sentences()
   




