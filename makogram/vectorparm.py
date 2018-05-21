from makogram.parmgen import Parm, MAX_GENS
from makogram.range import Range
from math import floor
from random import randint
import logging
logging.basicConfig(format='%(levelname)s:%(message)s',
                        level=logging.WARNING)
log = logging.getLogger(__name__)


class VectorParm(Parm):
        def __init__(self, name, generator_type, distr_type="uniform", desired="many", low=None, high=None, ave=None, dev=None, peak=None, from_set=None, per_row=3):
                """
                from_set is different here in a vector parm than it is in a Parm
                in Parm, it was a list of new objects, maybe strings or names or whatever
                in VectorParm, it is a list of Range objects.
                the length of this list should equal per_row
                since each point in the vector for the row will be generated from a Range object
                """

                Parm.__init__(self, name, generator_type, distr_type, desired, low, high, ave, dev, peak, from_set, per_row)
                assert from_set != None, "VectorParm from_set must be initalized"
        
        def generate(self, k=10000):
                if self.distr_type == "_cardioid":
                        sampling = self._cardioid_gen()
                        return sampling
                
                #Otherwise...
                # Generate the large sample size
                samples = []
                for j in range(k):
                        chunk = [] #initalize row
                        for i in range(self.per_row):
                                rng = self.from_set[i] #Range object

                                if self.distr_type == "normal":
                                        pt = rng.normal_pick(self.dist_args)

                                elif self.distr_type == "uniform":
                                        pt = rng.uniform_pick(self.dist_args)

                                elif self.distr_type == "right_slanted":
                                        pt = rng.right_slanted_pick(self.dist_args)

                                elif self.distr_type == "left_slanted":
                                        pt = rng.left_slanted_pick(self.dist_args)

                                else: #cardioid multicol or None
                                        print("[Log>: distr_type is {}. How did you get here?".format(self.distr_type))

                                chunk.append(round(pt,2))
                        samples.append(tuple(chunk))

                # Now reduce down
                sample_size = len(samples) #How many initial data points are there?
                interval_step = floor(sample_size / self.desired)
                samples.sort() #sorts by the first point in the vector
                reduced = [] #initalize the final set
                for i in range(0, sample_size, interval_step): #choose every nth
                        reduced.append(samples[i])
                log.debug("original sample size is {} and desired is {}, so the interval step is {} and the final set is {}".format(sample_size, self.desired, interval_step, len(reduced)))
                while len(reduced) != self.desired:
                        reduced.pop()
                assert len(reduced) == self.desired, "reduced size is {}, desired points is {}".format(len(reduced), self.desired)
                return reduced

        def _cardioid_gen(self):
                """
                favorites is a list of desirable pairings, in the form of a list of tuples of Range objects
                the tuple 'spans' the columns, so tuple[0] is a desirable point in subcol1,
                        and tuple[1] is a desirable point in subcol2

                non_favorites is similarly a list of tuples of Range objects
                """
                assert self.favorites != None, "Uh-oh, favorites set for _cardioid distribution is not set"
                assert self.non_favorites != None, "Uh-oh, non_favorites set for _cardioid distribution is not set"
                num_favs = int(.9*self.desired)
                num_outliers = int(.1*self.desired)
                while num_outliers + num_favs < self.desired:
                    num_outliers+= 1
                assert num_outliers + num_favs == self.desired, "Uh-oh, _cardioid distribution creating wrong size sample: {}".format(num_outliers+num_favs)
                
                grand_set = []

                # generate all the favorites pairings
                for _ in range(num_favs):
                        select = self.favorites[randint(0, len(self.favorites)-1)] #tuple of range objects
                        row = []
                        for r in select: #the tuple may span several subcolumns
                                pt = r.uniform_pick(self.dist_args)
                                row.append(round(pt, 2))
                        grand_set.append(tuple(row))

                # now generate all the outliers
                for _ in range(num_outliers):
                        select = self.non_favorites[randint(0, len(self.non_favorites)-1)] #tuple of Ranges
                        row = []
                        for r in select: #the tuple may span several subcolumns
                                pt = r.uniform_pick(self.dist_args)
                                row.append(round(pt, 2))
                        grand_set.append(tuple(row))
                
                return grand_set

"""
v = VectorParm("position", "one-by-one", distr_type="_cardioid", from_set=[Range(-4.55E+12, 1.08E+12), Range(-3.89E+12, 8.51E+11), Range(-5.79E+10, 1.28E+12)])
v.setFavorites([(Range(0.0, 5.0), Range(10.0, 15.0), Range(20.0, 25.0))])
v.setNonFavorites([(Range(30.0, 35.0), Range(40.0, 45.0), Range(50.0, 55.0))])
v.setup()
stuff = v.getFinalDataSet()
for point in stuff:
        print(point)
"""
