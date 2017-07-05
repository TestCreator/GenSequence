"""
Generate a sequence of records (tuples) where each 
column in the record comes from its own generating function, 
but the "colun" generators can share some state. 
"""

import random
import sys

#
#  Example: A sequence of natural numbers,
#  uniformly distributed in some range. 
#
def nat_seq(low=0, high=sys.maxsize):
    """
    A sequence of randomly chosen natural numbers, 
    independent of other columns. 
    """
    while (True):
        yield random.randint(low, high)

#
# Example:  A filter for duplicates
#
def dedup(f):
    def deduplicated(*args): 
        seen = set()
        stream = f(*args)
        while (True):
            trial = next(stream)
            while trial in seen:
                trial = next(stream)
            seen.add(trial)
            yield(trial)
    return deduplicated


#
# Names (firstname, lastname)
# (up to 100 unique)
#
def names():
    """
    Simple names with alliteration (easy to remember); 
    always a firstname lastname pair, without coverage 
    of less common patterns (Jr, von, etc).
    """
    with open("pools/names.txt", 'r') as names:
        for name in names:
            yield name.strip()


if __name__ == "__main__":
    unique_nats = dedup(nat_seq)
    count = 0
    for x in zip(unique_nats(0,15), unique_nats(0,15), names()): 
        print(x)
        count += 1
        if count > 10:
            break


# FIXME:
#    This currently does not behave well when one of the sequences
#    is exhausted.  If I set the limit above to 20, when there are only
#    15 unique naturals between 0 and 15, the program will hang.  What
#    I want instead is that the loop is broken (the 'for' stops) when any
#    of the sub-sequences is exhausted. 
    
