"""
While makogram uses the mako template engine to build strings, 
it should also be capable of building structures that are not strings. 
Here we'll try to build up a list of lists of strings. 
"""

import nose

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
from makogram import grammar

import random

## With Mako templates only

def small_int():
    return random.choice([1, 2, 3, 4, 5, 6, 7, 8, 9, 0])

def test_one_list():
    """Most basic case: one list of 5 integers"""
    g = grammar.Grammar()
    g.prod("S", small_int, reps=5, splice=grammar.nosplice)
    result = g.gen("S")
    log.info("5 one-digit integers: {}".format(result))
    assert len(result) == 5

def test_list_lambda():
    """Can I use lambdas to make expressions more compact?"""
    g = grammar.Grammar()
    g.prod("S", lambda : random.choice([1, 2, 3]),
               reps=5, splice=grammar.nosplice)
    result = g.gen("S")
    log.info("Little lambda, little lambda, won't you give me: {}"
                 .format(result))

def test_list_lists():
    """Nested lists --- by explicit call to g.gen"""
    g = grammar.Grammar()
    g.prod("Inner", lambda : random.choice([1, 2, 3]), reps=5,
               splice=grammar.nosplice)
    g.prod("S", lambda : g.gen("Inner"), reps=5,
               splice=grammar.nosplice)
    result = g.gen("S")
    log.info("5x5 list of 1-3: {}".format(result))
    assert len(result) == 5 and len(result[4]) == 5

def test_list_of_strings():
    """Mako template expansion nested within lists"""
    g = grammar.Grammar()
    g.prod("Animal", "dog")
    g.prod("Animal", "cat")
    g.prod("pet", "small furry ${Animal()}")
    g.prod("pet", "large ${Animal()}")
    g.prod("S", "${pet()}", reps=5, splice=grammar.nosplice)
    result = g.gen("S")
    log.info("Pets: {}".format(result))
    assert len(result) == 5


if __name__ == "__main__":
    nose.runmodule()

