# Makogram:  Generative grammars with Mako templating

Generate test data using grammars written primarily as Mako templates,
with additional logic in Python.  Essentially, the right hand side of a
grammar production can be represented by a Mako template.  A non-terminal
*T* is represented on the right-hand-side of a production as `${T()}`, which may be bound to a set of templates
(right hand sides) or to a single Python function which returns a string.
A Python function for a non-terminal may in turn render Mako templates
(i.e., templates and procedures may freely and recursively refer to each other). 

## Why?

Grammars are a convenient and powerful way to describe complex data structures as well as sequences of operations (e.g., a sequence of method calls to bring an object into a desired state for a test case).  There are many grammar-based test case generation tools.  The main objectives of this one are:

* Integrate smoothly with (Python) test case generators controlled by test case specifications in CSV form, such as those produced by genpairs.py.

* Have a very low entry barrier:  Free to use and extend, easy to understand, easy to install.  In particular makogram is intended to be suitable for student use.

## Why Mako?

We chose a Python-based template engine to keep the entry barrier low, particularly for student use.  Among Python-based template engines, we considered Jinja2 and Mako.

Jinja2 is widely used in the Flask microframework for web applications, but can also be used separately from Flask.  Widespread use and familiarity to many students were points in Jinja2's favor.  However, Jinja2 strongly encourages computation of all the data for a template in advance, with just one call to render a template.  It provides some very limited facility for calling back into Python code for computation of values (primarily for filtering text values).  The essence of grammar-based text generation is recursion.  It is not straightforward (as far as we can see) to implement recursive
templates in Jinja2.

Mako embodies a different philosophy:  If Python provides some functionality,
the templating engine should expose that functionality rather than reimplementing it differently.  In particular, it is relatively straightforward to make calls from Mako templates to Python functions, provided the Mako templates are provided an environment (namespace) in which the functions are visible.  This gives us the basic mechanism for encoding a BNF grammar as a set of mutually recursive templates, as well as allowing a terminal or non-terminal symbol to be bound to a Python function for ultimate flexibility.

## Makogram.grammar API

TBD: Describe the API

