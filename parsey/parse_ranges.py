import ply.lex as lex
import ply.yacc as yacc

tokens = ('RANGE', 'ARGDATA', 'NAME', 'OPENBRACKET', 'CLOSEBRACKET', 'OPENPAREN', 'CLOSEPAREN', 'NUMBER', 'COMMA', 'EQUALS', 'COLON') #all the possible tokens

def t_RANGE(t):
    r'Range'
    return t
def t_ARGDATA(t):
    r'low|lp|ave|dev|rp|high'
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

#def t_LOW(t):
#    r'low'
#    return t
#def t_LP(t):
#    r'lp'
#    return t
#def t_AVE(t):
#    r'ave'
#    return t
#def t_DEV(t):
#    r'dev'
#    return t
#def t_RP(t):
#    r'rp'
#    return t
#def t_HIGH(t):
#    r'high'
#    return t
t_COLON = r':'
t_ignore = ' \t'
def t_error(t):
        raise TypeError("Unknown text '%s'" % (t.value))

lex.lex()

def p_Rangeobj(p):
        "rang : NAME RANGE opener argset closer"
        l = False;
        u = False
        if p[3] == '(':
                l = True
        if p[5] == ')':
                u = True
        #p[0] = {"varname": p[1], "Rangeobj": "".join(str(n) for n in p[2:])} #varname, Range descriptor
        argset = p[4]
        construct = "Range({low}, {high}, exclusive_lower={l}, exclusive_upper={u}, ave={ave}, dev={dev}, right_peak={rp}, left_peak={lp}".format(l=l, u=u, **argset)
        p[0] = {"varname": p[1], "Rangeobj": construct}

def p_opener(p):
        """
        opener : OPENPAREN
        opener : OPENBRACKET
        """
        p[0] = p[1]
def p_closer(p):
        """
        closer : CLOSEPAREN
        closer : CLOSEBRACKET
        """
        p[0] = p[1]

def p_allargs(p):
        """
        argset : argset dp
        argset : dp
        """
        if len(p) == 2:
            p[0] = {**p[1], **p[2]}
        else:
            p[0] = p[1]

def p_arg(p):
        """
        dp : ARGDATA COLON NUMBER
        dp : ARGDATA COLON NUMBER COMMA
        """
        p[0] = {p[1]: p[3]}

def p_error(p):
    print("Syntax error at {} {} {} {}".format(p.value, p.type, p.lexpos, p.lineno))
    return None

parser = yacc.yacc()

def establish_parses(in_file, parse_engine):
    collected_parses = []
    f = open(in_file, 'r')

    for one_line in f:
        if one_line.startswith("%%"):
            break
        if not one_line.startswith(("#", " ", "\n")):
            print(one_line)
            try:
                tokens = parse_engine.parse(one_line.strip())
                collected_parses.append(tokens)
            except (TypeError, AttributeError) as e:
                pass
    return collected_parses

#PARSED_TOKENS = establish_parses("/Users/jamiezimmerman/Documents/GenSequence/simple_earthquaker.prm", parser)

#info = {"key1": PARSED_TOKENS}

NEW_TOKENS = parser.parse("low : 0.5")


print(NEW_TOKENS)

