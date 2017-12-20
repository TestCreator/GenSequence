from random import gauss, uniform, triangular, sample
from math import ceil
import logging
logging.basicConfig(format='%(levelname)s:%(message)s',
                        level=logging.WARNING)
log = logging.getLogger(__name__)

MAX_GENS = 100

def many(gens):
        """
        returns a proportion of MAX_GENS, the greatest number of data points, a calibration point
        """
        return int(.7 * gens)
def few(gens):
        """
        returns a proportion of MAX_GENS, to calibrate how many data points are needed
        """
        return int(.3 * gens)
def posint(x):
        """
        returns no negative numbers
        """
        return 0 if x<0 else x
def norm(args):
        """
        creates a data point with normal (gaussian) distribution
        needs an average and devation (mu and sigma)
        guarantees the point is in a certain range (low and high) if those args are specified
        """
        ave = args["ave"]
        dev = args["dev"]
        low = args["low"]
        high = args["high"]
        x = round(gauss(ave, dev))
        if low==None and high == None:
                return x
        else:
                while not low <= x <= high:
                        x = round(gauss(ave, dev))
                return x
def uni(args):
        """
        creates a data point with uniform distribution
        """
        low = args["low"]
        high = args["high"]
        return uniform(low, high)
def slanted(args):
        """
        creates a data point with slant, triangular probability
        """
        low = args["low"]
        high = args["high"]
        peak = args["ave"]
        return triangular(low, high, peak)

def days_of_week():
        return [str(day + time) for day in ["M", "T", "W", "R", "F"] for time in ["10:00-12:00", "12:00-2:00", "2:00-4:00", "4:00-6:00"]]
def names():
        nameslist = []
        with open("pools/names.txt", 'r') as names:
                for name in names:
                        nameslist.append(name.strip())
        return nameslist

# typemap is a mapping from string specifiers passed into Parm initialization to function references
typemap = {"many": many,
           "few": few,
           "normal": norm,
           "uniform": uni,
           "triangular": slanted}
class Parm:
        def __init__(self, distr_type, desired, generator_type, low=None, high=None, ave=None, dev=None, from_set=None, per_row=1):
                """
                breakdown~
                generator_type: string; "one by one" or "fixed-size-chunks"
                generator: to be defined later; the generator object that yields data points, either one by one or at fixed size chunks
                distr_type: string, how the accumulated data points are dispersed.
                vert_distribution: function mapped by string; type of relationship between each row's value; constrained to "normal", "uniform", "slanted"
                horiz_distribution: string; type of relationship of values inside a row; in Team Builder this is not used; may be unnecessary altogether
                from_set: list of what the randomly picked data values could be; by default, this is ints (the natural number line)
                        framework should also support for days/times of week, domains, usernames, English first names, timestamps, 
                        longitude/latitude coordinates, and floats. Other data types must be specified by the user, i.e. specialty strings
                desired: string; "many", "few", which is translated into an int specifying the number of data points desired;
                        if the generator type is one-by-one, this is the number of rows for which one data point will be generated
                        if the generator type is fixed-size-chunks, this the number of rows times the number of data points each row needs
                        the arg can also be an int if the user wants it to be hardcoded

                """
                self.generator_type = generator_type
                self.generator = None #to be defined in a later method
                self.distr_type = distr_type
                self.vert_distribution = typemap[distr_type] #this is a function reference
                self.horiz_distribution = None; #TODO: implement this
                self.dist_args = {"low": low, #these are the args passed to different distribution functions
                                  "high": high,
                                  "ave": ave,
                                  "dev": dev}
                self.from_set = from_set
                if type(desired) == int:
                        self.desired = desired
                else:
                        self.desired = typemap[desired](MAX_GENS)

                self.final_data_set = []
                self.per_row = per_row
                self.generated = 0 # Marks if the generator object yield data points has been created

                # Error checking
                # if low or high is specified, the other must be specified as well
                assert ((low==None and high==None) or (not low==None and not high==None)), "low and high arguments must both be specified"
                # ave must be between low and high
                if not ave==None:
                        assert (low <= ave <= high), "Bad statistical arguments, must be low <= ave <= high"
                #the deviation from average must be between low and high to make statistical sense
                if not dev==None and not ave==None:
                        assert ((ave + dev <= high) and (ave - dev >= low)), "Deviation too great, extends beyond min and max values"
                # if the generator type is specialized, it must have per_row specified
                if generator_type != "one-by-one":
                        assert not per_row == None, "Must supply from_set and per_row for specialty generators"
                        self.rows = self.desired
                        self.desired = self.desired * per_row
        
        def generate(self, k=100000):
                """
                generates the samples from either ints or a special set of data points like names or times
                creates 100000 points, sorts them, and systematically picks points so that they are evenly dispersed
                and maintains the distribution guaranteed by Law of Large Numbers
                """
                # Generate the large sample size
                if self.from_set == None:
                        samples = [self.vert_distribution(self.dist_args) for _ in range(k)]
                else:
                        samples = [self.from_set[self.vert_distribution(self.dist_args)] for _ in range(k)]
                # Now reduce down
                sample_size = len(samples) #How many initial data points are there?
                interval_step = ceil(sample_size / self.desired)
                samples.sort() #The sorted data points
                reduced = []
                for i in range(0, sample_size, interval_step):
                        reduced.append(samples[i])

                log.debug("original sample size is {} and desired is {}, so the interval step is {} and the final set is {}".format(sample_size, self.desired, interval_step, len(reduced)))
                assert len(reduced) == self.desired
                return reduced
        def setup(self):
                """
                calls the creation of data points, shuffles them, and stores them as a class data member
                """
                items = self.generate()
                self.final_data_set = sample(items, len(items))
 
        def distribute(self, data_set):
                """
                generator object creation for basic point-by-point generators
                """
                for point in data_set:
                        yield point

        def multipart_distribute(self, gene, outer, inner):
                """
                combines inner number of data points into one rendered package of information
                outer * inner = desired number of created points
                """
                for _ in range(outer):
                        chunk = ""
                        for _ in range(inner):
                                chunk += " " +next(gene)
                        yield chunk
        def next(self):
                """
                called upon a Parm object to get the next object from the generator
                if the generator has not been created, it is created before next is rendered
                if the generator has been created, it skips double creation and maintains its current place in iteration
                """
                if self.generated == 0:
                        if self.generator_type == "one-by-one":
                                self.generator = self.distribute(self.final_data_set)
                        else:
                                self.generator = self.multipart_distribute(self.distribute(self.final_data_set), self.rows, self.per_row)
                        self.generated = 1
                return next(self.generator)



times = Parm("normal", "many", "fixed-size-chunks", low=5, high=12, ave=8, dev=3, from_set=days_of_week(), per_row=5)
times.setup()
while True:
        try:
                print(times.next() + ",")
        except StopIteration:
                break
print("done")






        