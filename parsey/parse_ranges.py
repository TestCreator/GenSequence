import ply.lex as lex
import ply.yacc as yacc

tokens = ('RANGE', 'ARGDATA', 'NAME', 'OPENBRACKET', 'CLOSEBRACKET', 'OPENPAREN', 'CLOSEPAREN', 'NUMBER', 'COMMA', 'COLON') #all the possible tokens

def t_ARGDATA(t):
    r'low|lp|ave|dev|rp|high'
    return t
def t_RANGE(t):
    r'Range'
    return t

t_NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'
t_OPENBRACKET = r'\['
t_CLOSEBRACKET = r'\]'
t_OPENPAREN = r'\('
t_CLOSEPAREN = r'\)'
#t_EQUALS = r'='
def t_NUMBER(t):
        r'\d+[.,]?\d*'
        t.value = float(t.value)
        return t
t_COMMA = r'\,'
t_COLON = r':'
t_ignore = ' \t'
def t_error(t):
        raise TypeError("Unknown text '%s'" % (t.value))

lex.lex()

def p_rang(p):
        "rang : NAME RANGE opener argset closer"
        l = True if p[3] == '(' else False
        u = True if p[5] == ')' else False
        argset = p[4]
        construct = "Range({}, {}, ".format(argset['low'], argset['high'])
        del argset['low'], argset['high']
        for key in argset:
            construct += "{}={}, ".format(key, argset[key])
        construct += "exclusive_lower={l}, ".format(l=l)
        construct += "exclusive_upper={u})".format(u=u)
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

def p_argset(p):
        """
        argset : argset dp
        argset : dp
        """
        if len(p) == 3:
            p[0] = {**p[1], **p[2]}
        else:
            p[0] = p[1]

def p_dp(p):
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
    #f = open(in_file, 'r')
    for one_line in in_file:
        if one_line.startswith("%%"): #just stop here for now
            break
        if not one_line.startswith(("#", " ", "\n")):
            #print(one_line)
            try:
                t = parse_engine.parse(one_line.strip())
                collected_parses.append(t)
            except (TypeError, AttributeError) as e:
                pass
    mapping = {"ranges": collected_parses}
    return mapping

#PARSED_TOKENS = establish_parses("/Users/jamiezimmerman/Documents/GenSequence/simple_earthquaker.prm", parser)
#info = {"ranges": PARSED_TOKENS}


