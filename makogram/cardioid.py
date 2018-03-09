from makogram.parmgen import Parm
from makogram.range import Range 
from random import randint, sample

def pick(in_data, optargs):
        if isinstance(in_data, tuple):
                return tuple([round(item.uniform_pick(optargs),2) for item in in_data])

        elif isinstance(in_data, list):
                return [round(item.uniform_pick(optargs),2) for item in in_data]

        elif isinstance(in_data, Range):
                return round(in_data.uniform_pick(optargs),2)

class Cardioid:
        def __init__(self, first, second):
            """" a cardioid is composed to two columns (two parms), so store them away as class variables"""
            self.firstParm = first
            self.secondParm = second
        def setFromSet(self, new_set):
            self.from_set = new_set
        def setFavorites(self, fav):
            self.favorites = fav
        def setNonFavorites(self, non):
            self.non_favorites = non

        def generate(self):
            """ if a test vector contains both columns having a joint distribution, generate them together
            otherwise, generate the two parms disconnected
            """
            if self.firstParm.distr_type == "cardioid" and self.secondParm.distr_type == "cardioid":
                self.double_generate() #TODO - should return?
            else:
                self.single_generate()

        def double_generate(self):
            """
            from earthquaker.prm language:
            from_set: {Micro,Feelable,Great}*{Shallow,Mid,Deep}
            favorites: Micro*Shallow, Great*Deep, Feelable*Mid 
            not: Micro*Deep, Great*Shallow, Feelable*Deep, Feelable*Shallow 

            new_set is a list representing the cross product of all possibilities of the two columns
                it is a list of tuples of Range objects

            favorites is a list of desirable pairings, in the form of a list of tuples of Range objects
                the tuple 'spans' the columns, so tuple[0] is a desirable point in col1,
                and tuple[1] is a desirable point in col2

            non_favorites is similarly a list of tuples of Range objects
            """
            desired = self.firstParm.GetDesired() #how many pairs should we generate?
            num_favs = int(.9*desired) #90% of the sample is favorite
            num_outliers = int(.1*desired) #10% of sample is outliers
            while num_outliers + num_favs < desired:
                num_outliers+= 1
            assert num_outliers + num_favs == desired, "Uh-oh, cardioid distribution creating wrong size sample"
            
            # this will be a list of tuples of data points. 90% will be of favorites, and 10% outliers
            # this set has to be created this way, since the paired points can't be scrambled in individual columns
            # they must be scrambled before they are distributed out to the parms' final data sets
            grand_set = []
            # generate all the favorites pairings
            for _ in range(num_favs):
                #pick pair
                select = self.favorites[randint(0, len(self.favorites)-1)]
                firstpick = pick(select[0], self.firstParm.dist_args) #sometimes a range object
                secondpick = pick(select[1], self.secondParm.dist_args) #sometimes a tuple of ranges, but always a data set

                grand_set.append((firstpick, secondpick))

            # now generate all the outliers
            for _ in range(num_outliers):
                select = self.non_favorites[randint(0, len(self.non_favorites)-1)]
                firstpick = pick(select[0], self.firstParm.dist_args) #sometimes a range object
                secondpick = pick(select[1], self.secondParm.dist_args) #sometimes a tuple of ranges, but always a data set

                grand_set.append((firstpick, secondpick))

            #Now shuffle all around
            grand_set = sample(grand_set, len(grand_set))

            set1 = map(lambda point: point[0], grand_set) #get only the first points for col1
            set2 = map(lambda point: point[1], grand_set) #get only the second points for col2

            self.firstParm.setFinalDataSet(set1)
            self.firstParm.renew()
            self.secondParm.setFinalDataSet(set2)
            self.secondParm.renew()

            #and the points in rows are still paired up according to favorites or outliers!
        def single_generate(self):
            self.firstParm.setup()
            self.firstParm.scramble()
            self.secondParm.setup()
            self.secondParm.scramble()
