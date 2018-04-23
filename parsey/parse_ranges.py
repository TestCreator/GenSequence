import ply.lex as lex
import ply.yacc as yacc

tokens = ('RANGE', 'NAME', 'OPENBRACKET', 'CLOSEBRACKET', 'OPENPAREN', 'CLOSEPAREN', 'NUMBER', 'COMMA', 'EQUALS') #all the possible tokens

def t_RANGE(t):
    r'Range'
    return t
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

def p_Rangeobj(p):
        "rang : NAME RANGE opener NUMBER COMMA NUMBER closer"
        l = False;
        u = False
        if p[3] == '(':
                l = True
        if p[7] == ')':
                u = True

        p[0] = {"varname": p[1], "Rangeobj": "Range({lower_bound}, {upper_bound}, exclusive_lower={l}, exclusive_upper={u})".format(lower_bound=p[4], upper_bound=p[6], l=l, u=u)}

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

def establish_parses(in_file, parse_engine):
    collected_parses = []
    f = open(in_file, 'r')

    #TODO: iterate over lines - for now just stop at Global Declarations
    one_line = parse_engine.parse(f.readline().strip())
    print(one_line)
    collected_parses.append(one_line)
    #TODO: return list of parses, not just the one
    return one_line

PARSED_TOKENS = establish_parses("/Users/jamiezimmerman/Documents/GenSequence/simple_earthquaker.prm", parser)

