"""
python's builtin range object wasn't enough, so I built one that ranges floats instead of just ints.
It also has options for exclusive edge cases. By default, the Range is inclusive of both sides. Not very gracefully implemented, 
but it suffices for now. Does not support iteration. Provides for random generation pick within boundaries.

"""

EPSILON = .000001

import random # for random picks in the range
class Range:
        def __init__(self, lower, upper, exclusive_lower=False, exclusive_upper=False, ave=None, dev=None, left_peak=None, right_peak=None):
                assert lower < upper, "Bad Range: lower {} must be < upper {}".format(lower, upper)

                self.lower = lower
                self.upper = upper
                self.exclusive_lower = exclusive_lower
                self.exclusive_upper = exclusive_upper
                if exclusive_lower == True: #not just not none
                    self.low_epsilon = EPSILON
                else:
                    self.low_epsilon = 0 
                if self.exclusive_upper:
                    self.high_epsilon = EPSILON
                else:
                    self.high_epsilon = 0

                if ave == None: #if the user did not define
                    self.ave = (self.upper - self.lower)/2
                else:
                    self.ave = ave

                if dev == None: #if the user did not define
                    self.dev = (self.upper - self.ave)/4
                else:
                    self.dev = dev

                if left_peak == None:
                    self.left_peak = (self.ave + self.lower)/2
                else:
                    self.left_peak = left_peak

                if right_peak == None:
                    self.right_peak = (self.ave + self.upper)/2
                else:
                    self.right_peak = right_peak

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

        def uniform_pick(self, args):
                low = self.lower + self.low_epsilon
                high = self.upper - self.high_epsilon
                return random.uniform(low, high)
        
        def normal_pick(self, args):
                low = self.lower + self.low_epsilon
                high = self.upper - self.high_epsilon
                ave = args['ave'] or self.ave #if args is not specified, use data members by default
                dev = args['dev'] or self.dev 
                x = random.gauss(ave, dev)
                while not low <= x <= high:
                        x = random.gauss(ave, dev)
                return x

        def right_slanted_pick(self, args):
                low = self.lower + self.low_epsilon
                high = self.upper - self.high_epsilon
                peak = args['peak'] or self.right_peak
                return random.triangular(low, high, peak)

        def left_slanted_pick(self, args):
                low = self.lower + self.low_epsilon
                high = self.upper - self.high_epsilon
                peak = args['peak'] or self.left_peak
                return random.triangular(low, high, peak)

        def cardioid(self, args):
                pass

