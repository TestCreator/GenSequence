"""
Simple shakedown of grammar.py features, one by one. 
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

def test_string_template():
    """One rhs consisting only of a string"""
    pattern = "this is a test"
    g = grammar.Grammar()
    g.prod("S", pattern)
    result = g.gen("S")
    assert result == pattern

def test_mako_sub():
    g = grammar.Grammar()
    g.prod("S", "testing ${p2()} testing")
    g.prod("p2", "passing")
    result = g.gen("S")
    assert result == "testing passing testing"

def test_mako_choice():
    g = grammar.Grammar()
    g.prod("S", "testing ${p2()}")
    g.prod("p2", "A")
    g.prod("p2", "B")
    g.prod("p2", "C")
    result = g.gen("S")
    assert result in ["testing A", "testing B", "testing C"]

## With procedures

def foo():
    return "FOO"

def test_mixed_choice():
    g = grammar.Grammar()
    g.prod("S", foo)
    g.prod("S", "bar")
    has_foo = False
    has_bar = False
    for _ in range( 1000 ):
        s = g.gen("S")
        assert s=="FOO" or s=="bar"
        if s == "FOO": has_foo = True
        if s == "bar": has_bar = True
        if has_foo and has_bar:
            return
    assert False, "Didn't try both choices"

    
if __name__ == "__main__":
    nose.runmodule()

