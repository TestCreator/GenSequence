
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'CLOSEBRACKET CLOSEPAREN COMMA EQUALS NAME NUMBER OPENBRACKET OPENPAREN RANGErang : NAME NAME opener NUMBER COMMA NUMBER closer\n        opener : OPENPAREN\n        opener : OPENBRACKET\n        \n        closer : CLOSEPAREN\n        closer : CLOSEBRACKET\n        '
    
_lr_action_items = {'OPENBRACKET':([3,],[4,]),'NAME':([0,2,],[2,3,]),'$end':([1,10,11,12,],[0,-4,-1,-5,]),'OPENPAREN':([3,],[5,]),'NUMBER':([4,5,6,8,],[-3,-2,7,9,]),'COMMA':([7,],[8,]),'CLOSEPAREN':([9,],[10,]),'CLOSEBRACKET':([9,],[12,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'rang':([0,],[1,]),'closer':([9,],[11,]),'opener':([3,],[6,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> rang","S'",1,None,None,None),
  ('rang -> NAME NAME opener NUMBER COMMA NUMBER closer','rang',7,'p_Rangeobj','test.py',45),
  ('opener -> OPENPAREN','opener',1,'p_opener','test.py',58),
  ('opener -> OPENBRACKET','opener',1,'p_opener','test.py',59),
  ('closer -> CLOSEPAREN','closer',1,'p_closer','test.py',64),
  ('closer -> CLOSEBRACKET','closer',1,'p_closer','test.py',65),
]
