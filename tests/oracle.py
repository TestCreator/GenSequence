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


def test_mako_sub():
    g = grammar.Grammar()
    #This is a grammar of the test cases
    g.prod("S", "testing ${p2()} testing")
    g.prod("p2", "passing")
    g.prod("p2", "")
    result = g.gen("S")
    #This is a singular generated test case (input)
    #assert result == "testing passing testing"
    return result

def our_program(inp):
    ''' We secretly don't know anything about program execution'''
    if "passing" in inp:
        start = inp.index('p')
        end = inp.index('g') #.... We are lucky there are no other p's or g's in the word passing!
        inp[start:end] = ''
    return inp

def output_grammar():
    out = grammar.Grammar()
    #This is a grammar of the test case OUTPUT results
    out.prod("S", "testing ${p2()} testing")
    out.prod("p2", "")
    result = out.gen("S")
    return result

def check_oracle(input_case, output_case):
    ''' input_case is a test case
        output_case is the grammar it must follow'''

    print("\tChecking these...")
    print("\t" + input_case)
    print("\t" + output_case)
    #Oracle rules listed here:
    assert input_case == output_case, "Not Good!"
    print("All Good in the hood")

    
if __name__ == "__main__":
    tmp = test_mako_sub()
    print("THE INPUT IS:\t{}".format(tmp))
    prg = our_program(tmp)
    print("THE OUTPUT IS:\t{}".format(prg))

    print("CHECKING ORACLE")
    print(check_oracle(prg, output_grammar()))
    #nose.runmodule()

'''Comments:
when we check oracle, we check and compare 2 things:
    1. the output of the program
    2. the grammar the output must follow
The current example is limiting in two ways:
    1. the current grammar only generates one output - not
        the intended use case of a grammar. A grammar is a
        blue print not a comprehensive and limiting guideline
    2. the oracle checking is very simple - 
