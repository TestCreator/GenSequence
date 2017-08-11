"""
Where does max-uses apply?
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

## With Mako templates only

def test_max_with_kleene():
    """Max-uses should apply to the whole rhs"""
    g = grammar.Grammar()
    g.prod("p", "a b", weight=0)
    g.prod("p", "c", max_uses=2, min=2, max=5, weight=5)
    for _ in range(5):
        print( g.gen("p") )

    
    
# if __name__ == "__main__":
#    nose.runmodule()

test_max_with_kleene()

