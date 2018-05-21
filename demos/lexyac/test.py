import ply.lex as lex
import ply.yacc as yacc

tokens = ('RANGE', 'NAME', 'OPENBRACKET', 'CLOSEBRACKET', 'OPENPAREN', 'CLOSEPAREN', 'NUMBER', 'COMMA', 'EQUALS') #all the possible tokens

t_RANGE = r'Range'
t_NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'
t_OPENBRACKET = r'\['
t_CLOSEBRACKET = r'\]'
t_OPENPAREN = r'\('
t_CLOSEPAREN = r'\)'
t_EQUALS = r'='
def t_NUMBER(t):
        r'\d+[.,]?\d*'
        t.value = float(t.value)
        return t
t_COMMA = r'\,'
t_ignore = ' \t'
def t_error(t):
        raise TypeError("Unknown text '%s'" % (t.value))

lex.lex()

class Range:
        def __init__(self, lower, upper, exclusive_lower=False, exclusive_upper=False, ave=None, dev=None, left_peak=None, right_peak=None):
                assert lower < upper, "Bad Range: lower {} must be < upper {}".format(lower, upper)
                self.lower = lower
                self.upper = upper
                self.exclusive_lower = exclusive_lower
                self.exclusive_upper = exclusive_upper
        def __repr__(self):
                if self.exclusive_lower:
                        lowkey = "("
                else:
                        lowkey = "["
                if self.exclusive_upper:
                        highkey = ")"
                else:
                        highkey = "]"
                return "Range{}{},{}{}".format(lowkey, self.lower, self.upper, highkey)
        def __str__(self):
                return repr(self)

def p_Rangeobj(p):
        "rang : NAME NAME opener NUMBER COMMA NUMBER closer" #NUMBER COMMA NUMBER CLOSEPAREN"
        l = False;
        u = False
        if p[3] == '(':
                l = True
        if p[7] == ')':
                u = True

        if p[2] == 'Range':
                p[0] = {"varname": p[1], "Rangeobj": "Range({lower_bound}, {upper_bound}, exclusive_lower=l, exclusive_upper=u)".format(lower_bound=p[4], upper_bound=p[6])}

def p_opener(p):
        """
        opener : OPENPAREN
        opener : OPENBRACKET
        """
        p[0] = p[1]#
def p_closer(p):
        """
        closer : CLOSEPAREN
        closer : CLOSEBRACKET
        """
        p[0] = p[1]

def p_error(p):
    print("Syntax error at {} {} {} {}".format(p.value, p.type, p.lexpos, p.lineno))
    return None

parser = yacc.yacc()
line = "mass Range(0.57, 5.99]"
b = parser.parse(line)

