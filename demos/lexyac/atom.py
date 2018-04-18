import ply.yacc as yacc
import ply.lex as lex

tokens = (
    "SYMBOL",
    "COUNT"
)

t_SYMBOL = (
    r"C[laroudsemf]?|Os?|N[eaibdpos]?|S[icernbmg]?|P[drmtboau]?|"
    r"H[eofgas]?|A[lrsgutcm]|B[eraik]?|Dy|E[urs]|F[erm]?|G[aed]|"
    r"I[nr]?|Kr?|L[iaur]|M[gnodt]|R[buhenaf]|T[icebmalh]|"
    r"U|V|W|Xe|Yb?|Z[nr]")

def t_COUNT(t):
    r"\d+"
    t.value = int(t.value)
    return t

def t_error(t):
    raise TypeError("Unknown text '%s'" % (t.value,))

lex.lex()

class Atom(object):
    def __init__(self, symbol, count):
        self.symbol = symbol
        self.count = count
    def __repr__(self):
        return "Atom({}, {})".format(self.symbol, self.count)

# When parsing starts, try to make a "chemical_equation" because it's
# the name on left-hand side of the first p_* function definition.

def Print(tyype, t):
    i=0
    while True:
        try:
            tyype += ("\t" + str(t[i]))
        except:
            break
        i += 1
    print (tyype + "\tdone")

def p_species_list(p):
    "chemical_equation :  chemical_equation species"
    p[0] = p[1] + [p[2]]
    Print("species list ", p)


def p_species(p):
    "chemical_equation : species"
    p[0] = [p[1]]
    Print("species", p)


def p_single_species(p):
    """
    species : SYMBOL
    species : SYMBOL COUNT
    """
    if len(p) == 2:
        p[0] = Atom(p[1], 1)
    elif len(p) == 3:
        p[0] = Atom(p[1], p[2])
    Print("single species ", p)

        
def p_error(p):
    print("Syntax error at {}".format(p.value))
    return None
    
parser = yacc.yacc()

b = parser.parse("C60H60")
print(b)
print(type(b))
for item in b:
    print(type(item))
