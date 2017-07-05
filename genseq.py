"""
Generate a sequence of records (tuples) where each 
column in the record comes from its own generating function, 
but the "colun" generators can share some state. 
"""

import random
import sys
import logging

logging.basicConfig(format='%(levelname)s:%(message)s',
                        level=logging.DEBUG)
log = logging.getLogger(__name__)

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
#    with a limit on attempts
#
def dedup(f, limit=100):
    def deduplicated(*args): 
        seen = set()
        stream = f(*args)
        while (True):
            trial = next(stream)
            attempts=1
            while trial in seen:
                attempts += 1
                if attempts > limit:
                    log.debug("Dedup filter bailing after {} attempts".format(attempts))
                    raise StopIteration("{} failed attempts to generate a unique value".
                                            format(attempts))
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
        if count > 20:
            break


