from random import gauss, uniform, triangular, sample, choice, randint
from math import floor
from makogram.range import Range # for cardioid generation
import logging
logging.basicConfig(format='%(levelname)s:%(message)s',
                        level=logging.WARNING)
log = logging.getLogger(__name__)

MAX_GENS = 100
SEPARATOR = ","
THE_LIST = []
def count_frequency(raw_data):
        raw_data.sort()
        raw_data.append('sentinel')
        count = 0
        for i in range(0, len(raw_data)-1):
            if raw_data[i + 1] == raw_data[i]:
                count += 1
            else: #majors[major + 1] != majors[major]
                count += 1
                print ("Value {} has count {}".format(raw_data[i], count))
                count = 0

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
        guarantees the point is in a certain range (low and high) if thgigiose args are specified
        """
        ave = args["ave"]
        dev = args["dev"]
        low = args["low"]
        high = args["high"]
        x = gauss(ave, dev)
        if low==None and high == None:
                return x
        else:
                while not low <= x <= high:
                        x = gauss(ave, dev)
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
        peak = args["peak"]
        return triangular(low, high, peak)

def cardioid(args):
        pass

def _cardioid(args):
        pass

def days_of_week():
        return [str(day + time) for day in ["M", "T", "W", "R", "F"] for time in ["10:00 - 12:00", "12:00 - 2:00", "2:00 - 4:00", "4:00 - 6:00"]]

dayorder = {"M": 1,
            "T": 2,
            "W": 3,
            "R": 4,
            "F": 5}
def sort_by_days(dayset):
        """
        args:
        (str) dayset - string representation of one student's availability, time slots separated by comma
            ex: "T2:00-4:00,W4:00-6:00,T10:00-12:00,W12:00-2:00,R2:00-4:00"
        reorders these time slot availabilities by day and then by time, deleting duplicates
        implementation uses bubble sort
        """
        newset = list(set(dayset.split(","))) #sets delete duplicates
        n = len(newset)
        for i in range(n):
            for j in range(1, n):
                prev = dayorder[newset[j-1][0]]
                curr = dayorder[newset[j][0]]
                if prev > curr:
                    temp = newset[j-1]
                    newset[j-1] = newset[j]
                    newset[j] = temp
        return newset

def translate_desired(des):
        try:
            return int(des)
        except ValueError: #if the arg is of type string - hopefully it is "many" or "few" to accurately key into the typemap
            try:
                return typemap[des](MAX_GENS)
            except KeyError: #if the arg is not mapped to a function in typemap - passed in something bad as a symbolic test vector
                log.debug("*** You goose! you passed {} as a map into type map".format(des))

def names():
        nameslist = []
        with open("pools/names.txt", 'r') as names:
                for name in names:
                        nameslist.append(name.strip())
        return nameslist
def names_generator(li):
        for thing in li:
                yield thing

# typemap is a mapping from string specifiers passed into Parm initialization to function references
typemap = {"many": many,
           "few": few,
           "normal": norm,
           "uniform": uni,
           "right_slanted": slanted,
           "left_slanted": slanted,
           "cardioid": cardioid,
           "_cardioid": _cardioid}

class Parm:
        def __init__(self, name, generator_type, distr_type="uniform", desired="many", low=None, high=None, ave=None, dev=None, peak=None, from_set=None, per_row=1):
                """
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
                self.name = name
                self.generator_type = generator_type
                self.generator = None #to be defined in a later method
                self.distr_type = distr_type
                self.vert_distribution = typemap[distr_type] #this is a function reference
                self.horiz_distribution = None; #TODO: implement this
                self.dist_args = {"low": low, #these are the args passed to different distribution functions
                                  "high": high,
                                  "peak": peak,
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
                        assert per_row != None, "Must supply from_set and per_row for specialty generators"
                        self.rows = self.desired
                        self.desired = self.desired * per_row
        
        def setGeneratorType(self, gentype):
                self.generator_type = gentype
        def setGenerator(self, gene):
                self.generator = gene
        def setDistributionType(self, distr_type):
                self.distr_type = distr_type
                self.vert_distribution = typemap[distr_type]
        def setLow(self, low):
                self.dist_args[low] = low
        def setHigh(self, high):
                self.dist_args[high] = high
        def setAve(self, ave):
                self.dist_args[ave] = ave
        def setDev(self, dev):
                self.dist_args[dev] = dev
        def setPeak(self, peak):
                self.dist_args[peak] = peak
        def setFromSet(self, from_set):
                self.from_set = from_set
        def setDesired(self, desired):
                self.desired = translate_desired(desired)
                if self.generator_type != "one-by-one":
                    self.rows = self.desired
                    self.desired = self.desired * self.per_row
        def GetDesired(self):
                return self.desired
        def setFinalDataSet(self, final):
                self.final_data_set = final
        def getFinalDataSet(self):
                return self.final_data_set
        def setPerRow(self, per_row):
                self.per_row = per_row
        def renew(self):
                self.generated = 0
        def setFavorites(self, fav):
                """ fav is a list of Range objects. it can be a list of one Range """
                self.favorites = fav
        def setNonFavorites(self, non):
                """ non is a list of Range objects. it can be a list of one Range """
                self.non_favorites = non
        def generate(self, k=100000):
                """
                generates the samples from either ints or a special set of data points like names or times
                creates 100000 points, sorts them, and systematically picks points so that they are evenly dispersed
                and maintains the distribution guaranteed by Law of Large Numbers
                """
                if self.distr_type == "_cardioid":
                    sampling = self._cardioid_gen()
                    return sampling

                #Otherwise...
                # Generate the large sample size
                if self.from_set == None:
                        samples = [self.vert_distribution(self.dist_args) for _ in range(k)]
                else:
                        samples = [self.from_set[self.vert_distribution(self.dist_args)] for _ in range(k)]
                # Now reduce down
                sample_size = len(samples) #How many initial data points are there?
                interval_step = floor(sample_size / self.desired)
                samples.sort() #The sorted data points
                reduced = []
                for i in range(0, sample_size, interval_step):
                        reduced.append(samples[i])

                while len(reduced) != self.desired:
                    reduced.pop()
                log.debug("original sample size is {} and desired is {}, so the interval step is {} and the final set is {}".format(sample_size, self.desired, interval_step, len(reduced)))
                assert len(reduced) == self.desired
                return reduced


        def _cardioid_gen(self):
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
                    #pick point
                    select = self.favorites[randint(0, len(self.favorites)-1)] #Range object
                    pt = select.uniform_pick(self.dist_args)
                    grand_set.append(round(pt,2))

                # now generate all the outliers
                for _ in range(num_outliers):
                    select = self.non_favorites[randint(0, len(self.non_favorites)-1)] #Range object
                    pt = select.uniform_pick(self.dist_args)
                    grand_set.append(round(pt,2))
                
                return grand_set

        def setup(self):
                """
                calls the creation of data points, shuffles them, and stores them as a class data member
                """
                items = self.generate()
                self.final_data_set = items
                self.renew() #if reusing Parm object, pretend a generator hasn't been created before
        def scramble(self):
                items = self.final_data_set
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
                        for _ in range(inner-1):
                                chunk += next(gene) + SEPARATOR
                        chunk += next(gene)
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



        