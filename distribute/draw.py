"""
Drawing items from distributions and sequences. 

Even when drawing from a sequence, we will package
the functionality as functions rather than generators. 
In some cases those functions will really be 
callable objects. 
"""

import random
import sys
import logging

logging.basicConfig(format='%(levelname)s:%(message)s',
                        level=logging.DEBUG)
log = logging.getLogger(__name__)

# ##################
#
#  Wrapping functions in objects to either disallow or
#  encourage duplicate results
#
# ##################

class Dedup:
    """
    Remove duplicates from a distribution. 
    Similar to a decorator, but we wrap the function 
    in an object that also provides a "reset" method,
    and you can create more than one de-duplicated copy 
    of a function (using different names than the original 
    function) if you want to allow coincidences 
    across different sequences of values.

    Usage: 
      def f(x, y): ... 
      f_unique = Dedup(f)
      z = f(v, w)
    """
    def __init__(self, f, limit=100):
        """
        Create an object that acts like f, except with 
        no duplicates in return values.  If the underlying
        f returns a value that has been seen before, calling
        the deduplicated version will call f again, and again, 
        up until limit times to get a unique value. 
        If no unique value is obtained, a "StopIteration" exception
        will be thrown (but the callable cannot be used as a generator). 
        """
        self.f = f
        self.seen = set()
        self.limit = limit

    def reset(self):
        """
        Forget all the values that have been seen already.
        """
        self.seen = set()

    def __call__(self, *args):
        for _ in range(self.limit):
            result = self.f(*args)
            if result in self.seen: continue
            self.seen.add(result)
            return result
        raise StopIteration("{} failed attempts at unique value"
                                .format(self.limit))
    # FIXME: StopIteration is only useful within a generator.  Should
    # we throw a different exception?  Do something else?
    #


#
#  Return a prior result with a given probability.
#  (Converse of de-duplication.) 
#  Makes sense only if the result of f() does not depend on
#  the arguments, or if f is always called with the same arguments. 
#
class Coincidence: 
    """
    Add coincidences to the stream of results from a function:  
    With some probability between 
    0 and 1 (default 0.33), the next item generated is drawn at random 
    from the items that have already appeared.
    """

    def __init__(self, f, p=0.33):
        assert p > 0.0 and p < 1.0, (
            "Coincidence probability must be strictly between 0 and 1")
        self.f = f
        self.p = p
        self.seen = [ ]

    def __call__(self, *args): 
        if self.seen and random.random() > self.p:
            return random.choice(self.seen)
        result = self.f(*args)
        self.seen.append(result)
        return result

    
# If you want to use a function as an iterator or generator,
# streamify it.  Note that it will be called with the same
# arguments every time. 
#
def streamify(f):
    """
    Convert function f into a stream of results from 
    calling f repeatedly with the same arguments. 
    """
    def stream_of(*args):
        while True:
            yield f(*args)
    return stream_of

