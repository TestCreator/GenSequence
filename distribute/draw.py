"""
Drawing items from distributions and sequences. 

Even when drawing from a sequence, we will package
the functionality as functions rather than generators. 
In some cases those functions will really be 
callable objects. 
"""

import random
import sys
import os
import logging

logging.basicConfig(format='%(levelname)s:%(message)s',
                        level=logging.DEBUG)
log = logging.getLogger(__name__)

# ##################
#
# Some basic utilities that extend what the 'random'
# module gives us.  These were previously in rand_util.py.
#
# ##################

def sample_m_n(li,min,max):
    """Choose from m to n items, inclusive from li
    Examples: choose_m_n('abcdefg',3,5) => ['c', 'g', 'a']
              choose_m_n('abcdefg',3,5) => ['f','a','b','g','c']
   See also: random.sample.  The difference is that random.sample
   picks a sample of a fixed size, while sample_m_n picks a
   sample in a range of sizes. 
   """
    n_items = random.randrange(min,max+1)
    if n_items == 0:
        return [ ]
    sample=random.sample(li,n_items) 
    return sample

def sample_ordered_m_n(li,min,max):
    """Choose from m to n items, inclusive from li, 
    and return the in the same order as they appear in li. 
    Examples: choose_m_n('abcdefg',3,5) => ['a', 'c', 'g']
              choose_m_n('abcdefg',3,5) => ['a','b','c'', 'f', 'g']
   See also: random.sample.  The difference is that random.sample
   picks a sample of a fixed size, while sample_m_n picks a
   sample in a range of sizes. 
   """
    n_items = random.randrange(min,max+1)
    if n_items == 0:
        return [ ]
    indices = range(len(li))
    sample=random.sample(indices,n_items)  
    return [li[i] for i in sorted(sample)]

# Random string from alphabet --- based on Jamie's code for names
# and student ID numbers. 
# 
def rand_str(length,alphabet="abcdefghijklmnopqrstuvwxyz"):
    return ''.join(random.choice(alphabet) for _ in range(length))


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

#
# We have some precomputed streams of data as files.
# Currently 1:  A list of 100 names. 
#
def full_names():
    """Return a file descriptor from which up to 100 unique 
    alliterative names may be read.  

    These names do NOT cover
    all the variations in names, such as the 'von' prefix and 
    suffixes like Jr and III, so this pool of names should be
    used only where names are treated essentially as random strings
    with no program logic for name parsing.  
    """
    path = os.path.dirname(__file__) + "/pools/names.txt"
    return open(path)

