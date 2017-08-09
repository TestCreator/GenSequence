# Demos
These are for demonstrating and testing (in a loose sense) features of the test generation modules.  They are not *tests* strictly speaking because they do not include test oracles (there is no automation to checking their correctness), and they are not executed by the 'nosetests' script. 

## Contents

### `makogram_sort_gen.py`

Execute from the top-level project directory (so that the program can find the "pools" directory). Like this: 

`python3 demos/makogram_sort_gen.py`

Generates a Python program to test the built-in sort function of Python.  Not because we don't trust the built-in sort function, but as a simple demonstration of how some fixed boilerplate and some generated data can be merged with a grammar.  

We should get either exactly 10 test cases or something in the range of 1-5.  


