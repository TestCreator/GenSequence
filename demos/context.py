"""
Put sibling modules on the module search path. 
This is the approach recommended in 
  http://python-guide-pt-br.readthedocs.io/en/latest/writing/structure/
as versus my first approach which was 

  import nose
  from ..makogram import grammar

The import of ..makogram worked when running nosetests from the 
parent directory (genseq), like this 
   nosetests tests/makogram_test_basic.py
but did not work when running the module directly from the command 
line, from either the child or parent directory.  
"""
import os
import sys
sys.path.insert(0,
                os.path.abspath(
                    os.path.join(os.path.dirname(__file__), '..')))

