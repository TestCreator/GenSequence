"""
python's builtin range object wasn't enough, so I built one that ranges floats instead of just ints.
It also has options for exclusive edge cases. By default, the Range is inclusive of both sides. Not very gracefully implemented, 
but it suffices for now. Does not support iteration

"""
import random # for random picks in the range
class Range:
        def __init__(self, lower, upper, exclusive_lower=False, exclusive_upper=False):
                self.lower = lower
                self.upper = upper
                self.exclusive_lower = exclusive_lower
                self.exclusive_upper = exclusive_upper
                if self.exclusive_lower:
                    self.low_epsilon = .000001
                else:
                    self.low_epsilon = 0 
                if self.exclusive_upper:
                    self.high_epsilon = .000001
                else:
                    self.high_epsilon = 0

        def __repr__(self):
                if self.exclusive_lower:
                        lowkey = "("
                else:
                        lowkey = "["
                if self.exclusive_upper:
                        highkey = ")"
                else:
                        highkey = "]"
                return "Range{}{},{}{}".format(lowkey, self.lower, self.upper, highkey)

        def __str__(self):
                return repr(self)

        def __contains__(self, checkpoint):
                """ used for checking if an int is in Range (keyword in)
                r = Range(0.0, 9.7)
                  5 in r -> True
                  10.0 in r -> False
                """
                res1 = False
                res2 = False
                #check lower bound
                if self.exclusive_lower:
                        res1 ^= self.lower < checkpoint
                else:
                        res1 ^= self.lower <= checkpoint

                #check upper bound
                if self.exclusive_upper:
                        res2 ^= self.upper > checkpoint
                else:
                        res2 ^= self.upper >= checkpoint

                return res1 and res2

        def uniform_pick(self):
                low = self.lower + self.low_epsilon
                high = self.upper - self.high_epsilon
                return random.uniform(low, high)


r = Range(3.7, 5.0)
print(dir())
print(dir(r))
