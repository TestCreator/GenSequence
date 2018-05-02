"""
python's builtin range object wasn't enough, so I built one that ranges floats instead of just ints.
It also has options for exclusive edge cases. By default, the Range is inclusive of both sides. Not very gracefully implemented, 
but it suffices for now. Does not support iteration. Provides for random generation pick within boundaries.

"""

EPSILON = .000001

import random # for random picks in the range
from statistics import mean
class Range:
        def __init__(self, lower, upper, exclusive_lower=False, exclusive_upper=False, ave=None, dev=None, lp=None, rp=None):
                
                assert lower < upper, "Bad Range: lower {} must be < upper {}".format(lower, upper)

                self.lower = lower
                self.upper = upper
                self.exclusive_lower = exclusive_lower
                self.exclusive_upper = exclusive_upper
                if exclusive_lower == True: #not just not none
                    self.low_epsilon = EPSILON
                else:
                    self.low_epsilon = 0 
                if self.exclusive_upper == True:
                    self.high_epsilon = EPSILON
                else:
                    self.high_epsilon = 0

                self.ave = ave or mean([self.upper, self.lower])
                self.dev = dev or mean([self.upper, self.ave])/2
                self.lp = lp or mean([self.lower, self.ave])
                self.rp = rp or mean([self.upper, self.ave])
                
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

        #Getter Functions
        def low(self):
                return self.lower
        def high(self):
                return self.upper
        
        #Random functions
        def uniform_pick(self):
                low = self.lower + self.low_epsilon
                high = self.upper - self.high_epsilon
                return random.uniform(low, high)
        
        def normal_pick(self):
                low = self.lower + self.low_epsilon
                high = self.upper - self.high_epsilon
                x = random.gauss(self.ave, self.dev)
                while not (low <= x <= high):
                        x = random.gauss(self.ave, self.dev)
                return x

        def right_slanted_pick(self):
                low = self.lower + self.low_epsilon
                high = self.upper - self.high_epsilon
                return random.triangular(low, high, self.rp)

        def left_slanted_pick(self):
                low = self.lower + self.low_epsilon
                high = self.upper - self.high_epsilon
                return random.triangular(low, high, self.lp)

        def cardioid(self):
                pass
        def _cardioid(self):
                pass


        functions = {
            'uniform' : uniform_pick,
            'normal' : normal_pick,
            'right_slanted': right_slanted_pick,
            'left_slanted': left_slanted_pick,
            'cardioid': cardioid,
            '_cardioid': _cardioid
        }

