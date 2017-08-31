"""
Choices are supposed to be controlled by 
'weight' and 'max-uses' attributes.  When a 
production is one choice among right-hand-sides 
and also has repetition through the 'reps' or 
'max-uses' attributes, the choice attributes 
should apply to the whole production. 
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


def test_choice_alone():
    """Recursive productions guided by weight and max-uses"""
    g = grammar.Grammar()
    g.prod("A", "a", weight=0)
    g.prod("A", "${A()} x", weight=2, max_uses=5)
    log.info("Grammar: {}".format(g))
    result = g.gen("A")
    log.info("A -> a | A x, should be a x x x x x ; {}".format(result))
    assert result == "a x x x x x", "Got {}".format(result)

def test_choice_repeated():
    """Choice together with Kleene"""
    g = grammar.Grammar()
    g.prod("S", "${P() } ", reps=4)
    g.prod("P", "x", weight=0)
    g.prod("P", "y", weight=2, max_uses=2, reps=2)
    log.info("Grammar: {}".format(g))
    result = g.gen("S")
    log.info("Expecting 'yy yy x x', got {}".format(result))
    assert result == "yy yy x x ", "Got {}".format(result)
    
if __name__ == "__main__":
    nose.runmodule()
    

