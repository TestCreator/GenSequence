"""
CFG as test "grammar", but the right hand side of a 
production is anything with a 'render' method that takes
the grammar environment as a parameter. 

Most user code will use only the Grammar class, using Grammar.prod to 
create Renderables as the right hand sides of productions.  Some user 
code may need to create new subclasses of Renderable and provide them 
directly as the right hand sides of productions. 

Typical usage: 

from makogram import grammar
import random

g = grammar.Grammar()

# Production rules can be defined from a symbol
# like "NP" and a template using Mako syntax.  In a
# template, a non-terminal like NP would be invoked as ${NP()}
# Direct and indirect recursion is permitted. 
g.prod("Sentence", "The ${NP()}  ${VP()}")
g.prod("NP", "${Adjectives()} ${Noun()}")

# Repetition can be fixed with the reps keyword or
# selected randomly between a min and max bound
g.prod("Adjectives", "${Adj()}", min=0, max=3)

# Functions that return text can also be used as
# definitions of non-terminals
def noun():
    return random.choice(["dog", "cat"])
g.prod("Noun", noun)

def adj():
    return random.choice(["big ", "small "])
g.prod("Adj", adj)

# If multiple productions are given for the same
# non-terminal, it will be treated as a random choice,
# which may be limited and weighted.  
g.prod("VP", "chases mice", weight=3, max_uses=2)
g.prod("VP", "eats ${food()}", weight=1)

g.prod("food", "kibble", weight=2)
g.prod("food", "table scraps")
g.prod("food", "bugs")

# The max-uses holds across any number of calls to
# expand a term in the grammar.  "chases mice" will
# appear at most twice in the following sequence.
for _ in range(5):
    print(g.gen("Sentence"))

# Example output:
# The small small small  cat  chases mice
# The big  dog  eats kibble
# The big  dog  chases mice
# The small big  cat  chases mice
# The  cat  eats table scraps

"""

import mako.template      # For text productions --- use $(S()) to expand a non-terminal S

import random             # For selecting a|b and for a*

from decimal import Decimal
UNLIMITED = Decimal('Infinity')  # Just to print nicer than sys.max_size

import logging
logging.basicConfig(format='%(levelname)s:%(message)s',
                        level=logging.WARNING)
log = logging.getLogger(__name__)


def concat(x):
    """Default splicing function for Kleene"""
    return "".join(x)

def nosplice(x):
    """Identity function, mnemonically named for use with Kleene"""
    return x

class Grammar:
    """A grammar has a set of rules, 

    non-terminal ->  right hand side (rhs)
    where an rhs is a Renderable.  A Renderable is like a function 
    (it can be called) but has adDitional attributes weight and max-uses. 
    
    A renderable may be

    - Proc: a function wrapped in an object to hold the additional
    attributes

    - Template: a Mako template wrapped in an object to hold the
    additional attributes; its 'call' method calls the mako template
    render method, providing additional context from the grammar

    - Kleene: holds another renderable, which should return a string.  The
    weight and max-uses attribute control whether the Kleene object is
    selected, and additional attributes reps OR min and max control the
    number of times the wrapped object is expanded.

    - Choice: holds two or more renderables and chooses among them based
    on weight and max_uses.  A Choice object is created when more than
    one expansion is associated with the same non-terminal symbol.

    A renderable has a description (desc attribute), which may not be 
    the same as its name; the name -> rhs mapping is in the grammar, and
    the desc is in the renderable.  The game of a non-terminal is used 
    when we refer to grammar_env  (and in particular, when we pass that 
    grammar_env to the Mako template expander, where ${N()} in a template
    looks up N in grammar_env and calls it); that is the only use of 
    names, which means that we can build up parts of a right hand side 
    without naming some sub-expressions, e.g., making a Kleene star of a 
    Choice. 
    """
    
    def __init__(self):
        log.debug("Initializing Grammar object")
        self.grammar_env = { }
        self.counts = { }

    def _prod(self, name, rhs):
        """ 
        Associate production with non-terminal name. 
        At this point rhs should be a Renderable, and may 
        already have been wrapped in a Kleene.  We may 
        further wrap in a Choice if the non-terminal name 
        already has one or more rhs associated with it. 
        """
        if name not in self.grammar_env:
            log.debug("Adding {} -> {} to grammar_env"
                          .format(name, rhs))
            self.grammar_env[name] = rhs
            return
            
        # More than one RHS for this non-terminal, it should be a Choice.
        # Maybe it already is.
        log.debug("Prior mapping {} -> {}"
                      .format(name, self.grammar_env[name]))
        prior = self.grammar_env[name]
        if isinstance(prior, Choice):
            prior.add_choice(rhs)
            log.debug("Additional choice in mapping {} -> {}"
                          .format(name, self.grammar_env[name]))
            return

        # It's not already a Choice, so we'll create a Choice to wrap both
        # the old rhs and the new one.  The Choice object replaces the
        # individual rhs.
        choice = Choice(self)
        choice.add_choice(prior)
        choice.add_choice(rhs)
        self.grammar_env[name] = choice
        log.debug("New mapping to Choice {} -> {}"
                      .format(name, self.grammar_env[name]))


    ### Convenience method instantiates the different kinds
    ### of right-hand-sides depending on what is in the
    ### rhs.  If it has repetition parameters, we wrap it
    ### in a Kleene. 
    def prod(self, name, rhs, type="None", reps=None, min=0, max=None,
                 max_uses=UNLIMITED, weight=1, splice=concat, **kwargs):
        """
        Instantiate and record the appropriate kind of 
        right-hand-side. 

        Parameters
        ----------
        name : str
            The non-terminal symbol to be defined
        rhs :  str, Renderable, or callable
            right-hand-side, a possible expansion of the non-terminal
        reps : int, default=None
            if provided, the right-hand-side will be expanded reps times
        min : int, default=0
            if max is also provided, this is the minimum number of times 
            this rhs will be expanded
        max : int, default=None
            if provided (and if reps is not provided), then the 
            right hand side will be expanded between min and max times, 
            inclusive. 
        max_uses : int, default=999
            if there are other choices of rhs, then this one will be 
            chosen no more than max_uses times, across all expansions of 
            non-terminals in this grammar
        splice : function(list) default "".join(l)
            used only if reps or max is provided; how to splice 
            together the repeated elements constructed by Kleene. 
            The default is concatenation of strings.  Use grammar.nosplice
            to return a list. 
        """

        # If the right hand side isn't already a Renderable,
        # create a Renderable of the appropriate kind
        if isinstance(rhs,str):
            rhs = Template(self, rhs, weight=weight, max_uses=max_uses)
        elif isinstance(rhs, Renderable):
            pass
        elif callable(rhs):
            # But not a Renderable ... 
            log.debug("{} is callable".format(name))
            rhs = Proc(self, rhs, weight=weight, max_uses=max_uses)

        # At this point, if we don't have a Renderable,
        # we must have been passed something we can't
        # handle
        assert isinstance(rhs, Renderable), "Can't render {}".format(rhs)
        
        # If it has repetition parameters, we need to 
        # wrap it in a Kleene
        if reps or max:
            rhs = Kleene(self, rhs,
                             reps=reps, min=min, max=max,
                             weight=weight, max_uses=max_uses, 
                             splice=splice,
                             **kwargs)

        # Note that weight and max_uses, if given, will apply to the
        # fully wrapped rhs.  For example, we might have been given
        # a string, wrapped it in a Template, then wrapped that in a
        # Kleene ... and the weight and max_uses will apply to the
        # Kleene (which may then be further wrapped in a Choice by _prod). 
        self._prod(name, rhs, **kwargs)

    def __str__(self):
        """
        Print the grammar_env, which contains all the named 
        non-terminals in the grammar.  It may not contain 
        every piece of every rhs (non-terminals may have been 
        built up from sub-expressions that cannot be referred 
        to by name.
        """
        rep = "***GRAMMAR***"
        for symbol in self.grammar_env:
            rep += "\n{} -> {}".format(symbol, self.grammar_env[symbol])
        rep += "\n*** ------ ***"
        return rep
        #return str(self.grammar_env)

    def gen(self, name):
        """Apply the previously defined production rules and 
        return the derived string.

        Parameters
        ----------
        name : string
           A non-terminal symbol
        
        Returns
        -------
        A string derived from the non-terminal symbol 
        (typically through several recursive levels of expansion)
        """

        return self.grammar_env[name].render()

NAME_CNT = 0
def gen_name(prefix="N"):
    global NAME_CNT
    NAME_CNT += 1
    return "{}_{}".format(prefix,NAME_CNT)

class Renderable:
    """
    Abstract parent of all renderables. 
    Subclass this with a class that overrides the 'render' method
    and optionally overrides the '__init__' method (e.g., if you need
    the grammar object as context).   

    NOTE: If a keyword argument (weight, desc, or max_uses) appears in 
    the argument list of a subclass, it must be explicitly passed
    through the super().__init__ call, else the provided argument 
    will be overridden by a default value. 
    """
    def __init__(self, weight=1,max_uses=UNLIMITED, desc=None):
        log.debug("Initializing Renderable object")
        self.weight = weight
        self.max_uses = max_uses
        self.desc = desc or gen_name()

    def render(self):
        assert False, "Render method not implemented in {}".format(type(self))


    def __call__(self):
        """Calling the object is like calling the render method"""
        return self.render()

    def __str__(self):
        return self.desc

    def __repr__(self):
        max = self.max_uses
        if max == UNLIMITED : max = "_"
        return "{}[w:{}/mx:{}]".format(self.desc, self.weight, max)


class Proc(Renderable):
    """
    Turn any zero-argument callable into a renderable by wrapping it 
    in an object.  Note the grammar argument is not actually used; 
    it is here just for consistency with the other Renderable 
    constructors.  
    """
    def __init__(self, grammar, f, **kwargs):
        log.debug("Initializing Proc object")
        super().__init__(**kwargs, desc=str(f))
        self.f = f
        
    def render(self):
        log.debug("Rendering wrapped function")
        return self.f()

        
class Template(Renderable):
    """
    Essentially a Mako template, except that we carry a reference 
    to the Grammar object for rendering. 
    """

    def __init__(self, grammar, pattern, **kwargs):
        log.debug("Initializing Template object")
        super().__init__(**kwargs, desc=pattern)
        self.grammar = grammar
        self.template = mako.template.Template(pattern)

    def render(self):
        env = self.grammar.grammar_env
        try:
            result = self.template.render(**env)
            return result
        except TypeError as err:
            ## This is typically because of a reference to a symbol
            ## that has not been defined, e.g., a misspelled symbol 
            type_env = [ ( sym, type(sym) ) for sym in env.keys()]
            log.error("Failed to expand '{}' with symbols {}"
                          .format(self.template.source, type_env))
            raise err

class Kleene(Renderable):
    """
    A production thatis repeated some number of times, 
    either an absolute (reps) or a range (min,max).

    The default "splice" function concatenates strings. 
    To return a list, set splice to lambda x: x or grammar.nosplice
    """

    def __init__(self, grammar, term,
                     reps=None, min=0, max=9,
                     splice=concat, **kwargs):
        log.debug("Initializing Kleene object r{}/{}-{}"
                    .format(reps, min, max))

        if reps:
            desc = "({})^{}".format(term.desc,reps)
        else:
            desc = "({})^{}-{}".format(term.desc,min,max)
        super().__init__(**kwargs, desc=desc)

        self.grammar = grammar
        self.term = term
        self.reps = reps
        self.min = min
        self.max = max
        self.splice=splice
        
    def render(self):
        if self.reps:
            reps = self.reps
        else:
            reps = random.randint(self.min, self.max)
        l = [ self.term.render() for _ in range(reps) ]
        log.debug("Kleene render to {}".format(l))
        return self.splice(l)


class Choice(Renderable):
    """
    A set of production choices.  Each choice is a Renderable.  
    There must be at least one choice. 
    The render function selects one choice based on weight and 
    limits. 
    """
    def __init__(self, grammar,  **kwargs):
        log.debug("Initializing Choice object")
        super().__init__(**kwargs)
        self.grammar = grammar
        self.choices = [ ]


    def add_choice(self, choice):
        self.choices.append(choice)
        self.desc="{}|{}".format(self.desc,choice.desc)

    def render(self):
        counts = self.grammar.counts
        choices = self.choices

        log.debug("Choosing from: {}".format(choices))
        log.debug("Counts prior to choice: {}".format(counts))

        allowed = [ ]
        for choice in choices:
            if choice.desc not in counts:
                log.debug("Initializing count for {}".format(choice.desc))
                counts[choice.desc] = 0
            if choice.max_uses > counts[choice.desc]:
                log.debug("Allowing {} with max uses {} of {}"
                           .format(choice.desc[0:10],
                                   choice.max_uses, counts[choice.desc]))
                allowed.append(choice)
        if allowed:
            choices = allowed
            log.debug("Unlimited choices narrowed to ... {}".format(choices))
        else:
            log.debug("All choices have limited out")
        if len(choices) == 1:
            log.debug("Only one choice, so we'll take it")
            choice = choices[0]
            counts[choice.desc] += 1
            return choice.render()

        log.debug("Counts after narrowing choices: {}".format(counts))

        # Choose among remaining choices by weight
        weight_sum = 0.0
        for choice in choices:
            weight_sum += choice.weight
        threshold = random.random() * weight_sum
        for choice in choices:
            if choice.weight >= threshold:
                counts[choice.desc] += 1
                log.debug("Rendering '{}'".format(choice.desc))
                return choice.render()
            threshold -= choice.weight
        assert False, "Exhausted choices!"
        



