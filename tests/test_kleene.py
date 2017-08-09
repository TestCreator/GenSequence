"""
A unit test of the Kleene class, apart from the rest of the 
grammar apparatus. 
"""

import nose

import logging
logging.basicConfig(format='%(levelname)s:%(message)s',
                        level=logging.WARNING)
log = logging.getLogger(__name__)

## Ridiculous path hack so that this can work both within and
## outside of nosetests, locally and from the main project folder.
## 
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from makogram import grammar

g = grammar.Grammar()
term = grammar.Template(g, "T")

def test_reps_only():
    """reps indicates the exact numberr of repetitions"""
    kleene = grammar.Kleene(g, term, reps=3)
    out = kleene.render()
    log.debug("(T):3 => {}".format(out))
    assert out == "TTT"

def test_range_only():
    """Min and max indicate a range, closed on both ends"""
    kleene = grammar.Kleene(g, term, min=0, max=2)
    has_0 = False
    has_1 = False
    has_2 = False
    # We should generate each possibility with far less than
    # 10,000 tries
    for _ in range(10000):
        out = kleene.render()
        log.debug("(T):0-2 => '{}'".format(out))
        assert 0 <= len(out) <= 2 and out == "T" * len(out)
        if len(out) == 0 : has_0 = True
        if len(out) == 1 : has_1 = True
        if len(out) == 2 : has_2 = True
        if has_0 and has_1 and has_2 : return
    assert False, "Kleene did not generate all lengths 0..2"
    
if __name__ == "__main__":
    nose.runmodule()
    

