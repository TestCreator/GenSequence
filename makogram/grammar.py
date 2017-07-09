"""
Experimenting with Mako templating engine, potentially useful with 
test concretization and test sequence generation. 

Why Mako? Although I am more familiar with Jinja2 templating, 
the philosophy of Jinja2 is "minimize logic in templates."  I 
think that may be a good approach for web pages, but for test 
data generation it is just wrong.  Two things I want, which 
Jinja2 make difficult, are: 
  - Calling out to arbitrary Python functions to obtain data values. 
    Jinja2 is really designed for computing all the values to fill 
    in a template, then rendering the template. That is unnatural for 
    test data generation. 
  - Recursive templates.  I want a slot in a template to be potentially 
    filled by another template. 

Together, these two features should give me the basic tools to write 
generative grammars with both non-terminals and terminals controlled by 
Python code.  

Problem: How do I export functions into the scope of 
templates?   Flask does something similar with decorators ... 
can I have @context ? 

Answers: 
  The Flask example is useful ... The procedural attachment 
below (method procdef) is like the 'route' decorator in 
Flask. By wrapping the function within the the object, we should 
also get access to object fields.  The state of derivation 
poses a problem similar to request contexts in Flask, and the 
context field (and stack) is intended to be used in a similar 
but simpler way --- within a single derivation, we can stash 
and retrieve state information such as how many times a given 
production has been expanded (to limit recursion).  We do *not* 
handle multi-threading or other interleaving of derivations 
from the same grammar, so our context juggling can be a simple
stack, simpler than Flask's management of contexts. 

So let's see how hard that is in practice ... 
"""

from mako.template import Template
import random

class Grammar:
    """
    A generative grammar implemented as a set of 
    Python functions and templates. 
    """
    def __init__(self):
        self.grammar_env = { }  # For functions & attributes we want to pass to Mako
        #
        # Dynamic context of generation
        self.context = None
        self.ctx_stack = [ ]

    def procdef(self, name):
        """Make this function visible to Mako templates
           (a 'procedural' non-terminal
        """
        def decorate(f):
            self.grammar_env[name] = f
            return f
        return decorate

    def term(self, name, productions):
        """
        Define a term in the grammar
        Model of name ::= p1 | p2 | ... | pn 
        where  p1, p2, ... pn are 
        the right-hand sides.  If the productions 
        are unweighted (the only option for now), we 
        make a uniformly random choice among them. 

        This is a method, not a decorator.  It installs 
        a function the non-terminal name in the grammar_env. 
        """
        right_hands = [ Template(p) for p in productions ]
        n_choices = len(productions)
        def f():
            choice_index = int(random.random() * n_choices)
            choice = right_hands[choice_index]
            return choice.render(**self.grammar_env)
        self.grammar_env[name] = f

    def gen(self,term):
        """
        Interpret 'term' as a template to be expanded. 
        This is a top-level method that begins generating a new 
        sentence in the grammar.  It establishes a context for 
        the current sentence, which may include state information like 
        current depth of recursion, counts of various terms, etc. 
        Do not call this recursively from within the grammar! 
        """
        if self.context:
            print("Warning: Recursive call to 'gen'")
        self.ctx_stack.append(self.context)
        self.context = {}
        sentence = self._expand(Template(term))
        self.context = self.ctx_stack.pop()
        return sentence 

    def _expand(self,template):
        """Expand the template in the context of the 
        functions that have been defined as non-terminals
        """
        return template.render(**self.grammar_env)

