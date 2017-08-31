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
#  Example: An infinite sequence of natural numbers,
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
# Example: Decorator converts a function
#   into an infinite stream. Note the function
#   will be called with the same arguments
#   on each call, so this will not work for
#   functions that should respond to changing
#   state.
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
# Example:  A filter for duplicates
#    with a limit on attempts
#
def dedup(f, limit=100):
    """
    Decorator that removes duplicates from a stream.  
    If a subsequence of limit (default 100) items in 
    the stream have already been observed, dedup will
    conclude that the stream has been exhausted.  It 
    could be wrong, but false alarms of exhaustion should 
    occur rarely for limits greater than 10, except in 
    cases where the stream is *almost* exhausted of 
    unique values (e.g., if the stream randomly draws from 
    a collection of 100 unique values, and we have already 
    seen 85 of them). 
    """
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
            yield trial
    return deduplicated

#
#  The converse of deduplicating ---
#      reuse a prior value with probability p
#
def coincidence(f, p=0.33):
    """
    Add coincidences to a stream:  With some probability between 
    0 and 1 (default 0.33), the next item generated is drawn at random 
    from the items that have already appeared.
    """
    assert p > 0.0 and p < 1.0, "Coincidence probability must be strictly between 0 and 1"
    def with_coincidence(*args):
        seen = [ ]
        stream = f(*args)
        while True:
            if seen and random.random() > p:
                yield random.choice(seen)
            else:
                item = next(stream)
                seen.append(item)
                yield item
    return with_coincidence

#
# Weighted, limited choice of elements from
# two or more streams. Direct analogue to
# the way we choose among productions for a
# non-terminal in makogram.grammar.
# 
# We need to keep track of how many times each
# production has been used, and we don't want to be
# passing it around everywhere all the time, so we'll
# keep a global context.  We may add a context stack
# or other context-swapping mechanism later. 
#
#
context = { "counts": { } }

def prior_uses(stream):
    counts = context["counts"]
    return counts.get(stream,0)

def incr_uses(stream):
    counts = context["counts"]
    if stream in counts:
        counts[stream] += 1
    else:
        counts[stream] = 1

def choice(name, stream, max_uses=99999, weight=1):
    """
    This stream may be used up to max_uses times in 
    a context, and if enabled will be chosen with 
    weight weight (relative to other choices). 
    """
    return { "name": name, "stream": stream,
             "max_uses": max_uses, "weight": weight }


def choose( choices ):
    """
    Each element of choices is a choice structure; here we 
    choose among them by limits and by weight. 
    Compare to Grammar.choose in makogram.grammar. 
    """
    allowed = [ ]
    for choice in choices:
        if prior_uses(choice["stream"]) < choice["max_uses"]:
            allowed.append(choice)
    if allowed:
        choices = allowed
    else:
        log.debug("All choices have limited out")
    if len(choices) == 1:
        ch = choices[0]
        name = ch["name"]
        log.debug("Only one choice, so we'll take {}".format(name))
        stream = cho["stream"]
        incr_uses(stream)
        result = next(stream)
        log.debug("Generate element {}".format(result))
        yield result
    # Multiple choices left ... weighted selection
    weight_sum = 0.0
    for choice in choices:
        weight_sum += choice["weight"]
    threshold = random.random() * weight_sum
    for ch in choices:
        if ch["weight"] >= threshold:
            stream = ch["stream"]
            name = ch["name"]
            log.debug("Weighted choice of stream {}".format(name))
            incr_uses(stream)
            result = next(stream)
            log.debug("Generate element {}".format(result))
            yield result
        threshold -= choice["weight"]
    assert(False, "Exhausted choices!")
            
        

#
# Names (firstname, lastname)
# (up to 100 unique)
#
def names():
    """
    Simple names with alliteration (easy to remember); 
    always a firstname lastname pair, without coverage 
    of less common patterns (Jr, von, etc).

    This sequence is deterministic:  Although the pool 
    of names was generated randomly, we are reading from
    this fixed pool in sequential order.  Good for test 
    reproducibility (useful in debugging), bad if you 
    want to produce a number of test suites that together 
    cover more possible combinatons than a single test suite. 
    """
    with open("pools/names.txt", 'r') as names:
        for name in names:
            yield name.strip()


if __name__ == "__main__":
    unique_nats = dedup(nat_seq)
    count = 0
    un = unique_nats(0,15)
    cn = coincidence(nat_seq,0.5)
    cnames = coincidence(names)
    for x in zip(un, cn(0,15), cnames()): 
        print(x)
        count += 1
        if count > 20:
            break


