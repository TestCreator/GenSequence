class Range:
        def __init__(self, lower, upper, exclusive_lower=False, exclusive_upper=False):
                self.lower = lower
                self.upper = upper
                self.exclusive_lower = exclusive_lower
                self.exclusive_upper = exclusive_upper

        def __repr__(self):
                lowkey = ""
                highkey = ""
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