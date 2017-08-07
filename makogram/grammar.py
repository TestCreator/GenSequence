"""
CFG as test "grammar", but the right hand side of a 
production is anything with a 'render' method that takes
the grammar environment as a parameter. 

"""

import mako.template      # For text productions --- use $(S()) to expand a non-terminal S

import random             # For selecting a|b and for a*

from decimal import Decimal
UNLIMITED = Decimal('Infinity')  # Just to print nicer than sys.max_size

import logging
logging.basicConfig(format='%(levelname)s:%(message)s',
                        level=logging.DEBUG)
log = logging.getLogger(__name__)


class Grammar:
    """A grammar has a set of rules, 

    non-terminal ->  right hand side (rhs)
    where an rhs is a Renderable.  A Renderable is like a function 
    (it can be called) but has additional attributes weight and max-uses. 
    
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
        Production.  Called indirectly through 
        one of the convenience methods below. 
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


    ### Convenience methods instantiate the different kinds
    ### of right-hand-sides
    def prod(self, name, rhs):
        """
        Instantiate and record the appropriate kind of 
        right-hand-side. 
        """
        if isinstance(rhs,str):
            self._prod(name, Template(self,rhs))
        elif isinstance(rhs,Proc):
            self._prod(name,rhs)
        elif callable(rhs):
            print("{} is callable".format(name))
            wrapped = Proc(rhs)
            print("All wrapped up")
            self._prod(name, wrapped)
            print("And associated with its name")

    def __str__(self):
        """
        Print the grammar_env, which contains all the named 
        non-terminals in the grammar.  It may not contain 
        every piece of every rhs (non-terminals may have been 
        built up from sub-expressions that cannot be referred 
        to by name.
        """
        return str(self.grammar_env)

    def gen(self, name):
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
        return "{}[{}/{}]".format(self.desc, self.weight, self.max_uses)


class Proc(Renderable):
    """
    Turn any zero-argument callable into a renderable by wrapping it 
    in an object. 
    """
    def __init__(self, f, **kwargs):
        log.debug("Initializing Proc object")
        self.f = f
        super().__init__(**kwargs)
        
    def render(self):
        print("Rendering wrapped function")
        return self.f()

        
class Template(Renderable):
    """
    Essentially a Mako template, except that we carry a reference 
    to the Grammar object for rendering. 
    """

    def __init__(self, grammar, pattern, **kwargs):
        log.debug("Initializing Template object")
        self.grammar = grammar
        self.template = mako.template.Template(pattern)
        super().__init__(**kwargs, desc=pattern)

    def render(self):
        return self.template.render(**self.grammar.grammar_env)

class Choice(Renderable):
    """
    A set of production choices.  Each choice is a Renderable.  
    There must be at least one choice. 
    The render function selects one choice based on weight and 
    limits. 
    """
    def __init__(self, grammar,  **kwargs):
        log.debug("Initializing Choice object")
        self.grammar = grammar
        self.choices = [ ]
        super().__init__(**kwargs)

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
                return choice.render()
            threshold -= choice.weight
        assert False, "Exhausted choices!"
        



