"""
Simple test of generating sentences with makogram grammar

"""
from makogram.grammar import Grammar
import random 

g = Grammar()


# Attempt to simulate a generative grammar for
#   Expr ::=  small_int
#   Expr ::=  Expr + Expr
#
#   We define the symbols in two different ways: 
#   1.  We define Expr using grammar rules. 
#   2.  We define small_int procedurally so that we
#       can use the Python random library within it.
#


# Grammar rule

# g.term("expr", [
#        "${small_int()}",
#        "(${expr()} + ${expr()})"
#     ])

# # Procedural rule

# @g.procdef("small_int")
# def random_int():
#     if "count" not in g.context:
#         g.context["count"]=1
#     else:
#         g.context["count"] += 1
#     return g.context["count"]
#     # return random.randrange(-10,10)

# print(g.gen("${ expr() }"))


g.term("sentence", [
    "${article()} ${noun_phrase()} ${intransitive()}",
    "${article()} ${noun_phrase()} ${transitive()} ${article()} ${noun_phrase()}"])

g.term("noun_phrase", ["${adj()} ${noun_phrase()}",
                    "${noun()}"])

@g.procdef("article")
def article():
    return random.choice(["the", "a"])

@g.procdef("noun")
def noun():
    return random.choice(["ball", "man", "house", "squirrel"])

@g.procdef("adj")
def adjective():
    return random.choice(["big", "green", "brown", "scary"])

@g.procdef("intransitive")
def intransitive():
    return random.choice(["eats", "sleeps", "falls down"])

@g.procdef("transitive")
def transitive():
    return random.choice(["eats", "builds", "hits", "likes", "throws"])

print(g.gen("${sentence()}."))
