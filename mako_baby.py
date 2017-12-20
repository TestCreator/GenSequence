from makogram.grammar import Grammar
from random import gauss, triangular, choice, vonmisesvariate, uniform, sample
from statistics import mean
from math import ceil

"""
TWO METHODS:
1) sort the raw values, say there are 10 thousand of them.
        then if you want 100 of them, pick every 100th data point
2) specify how many data points you want, say 100. that's how many
        buckets you want. say 10 thousand data points with 60 buckets,
        interval = len(datapoints)/buckets
        range: 0~interval
                interval~interval+=interval, and so on
        Then pick the average of every bucket
"""

""" Globals - needed for calibration of the words "many", "few", and so on
"""
MAX_GENERATIONS = 100 #or this comes from the user - it likely must!
days = ["M", "T", "W", "R", "F"]
times = ["10:00-12:00", "12:00-2:00", "2:00-4:00", "4:00-6:00"]
all_free_times = [str(day + time) for day in days for time in times]


""" Random functions - normal, uniform, slanted, etc """
# returns non-negative. gaussian function may return a negative; ensure this never enters the data set
def posint(x):
        return 0 if x<0 else x
# returns a gaussian point - nonnegative integer
def norm(ave, dev, maxval=None):
        x = round(posint(gauss(ave, dev)))
        if maxval == None:
                return x
        else:
                while x > maxval:
                        x = round(posint(gauss(ave, dev)))
                return x

def generation(rv, average, deviation, maxval=None, k=100000, from_set=None):
        if from_set == None:
                samples = [rv(average, deviation, maxval) for _ in range(k)]
        else:
                samples = [from_set[rv(average, deviation, maxval)] for _ in range(k)]
        return samples

def reduce_down(raw_vals, desired):
        sample_size = len(raw_vals) #How many initial data points are there?
        interval_step = ceil(sample_size / desired)
        raw_vals.sort() #The sorted data points
        reduced = []
        for i in range(0, sample_size, interval_step):
                reduced.append(raw_vals[i])

        print("original sample size is {} and desired is {}, so the interval step is {} and the final set is {}".format(sample_size, desired, interval_step, len(reduced)))
        assert len(reduced) == desired
        return reduced

def distribute(data_set):
        for point in data_set:
                yield point

def multipart_distribute(gene, outer, inner):
        for _ in range(outer):
                chunk = ""
                for _ in range(inner):
                        chunk += next(gene)
                yield chunk



""" ----------------------------------------------------------------------
TeamBuilder Grammar """
desired_num_students = int(.7*MAX_GENERATIONS)
skill_level_small_value_set = reduce_down(generation(norm, 3, 2, maxval=5), desired_num_students)
reshuffled_skill_levels = sample(skill_level_small_value_set, len(skill_level_small_value_set))
skill_levels_generator = distribute(reshuffled_skill_levels) #this variable is a generator, call next(skill_levels_generator) to get value one by one

ave_slots_per_student = 5
desired_free_times_points = desired_num_students * ave_slots_per_student #guessing students on average have 5 free time slots during the week
sorted_free_times_small_value_set = reduce_down(generation(norm, 10, 3, maxval=19, from_set=all_free_times), desired_free_times_points)
reshuffled_free_times = sample(sorted_free_times_small_value_set, len(sorted_free_times_small_value_set))
free_times_basic_generator = distribute(reshuffled_free_times)
free_times_adv_generator = multipart_distribute(free_times_basic_generator, desired_num_students, ave_slots_per_student) #generator, call next()

tg = Grammar()
tg.prod("Classroom", "${Student()}", reps=desired_num_students) #reps should be class_size
tg.prod("Student", "other stuff,${skill_levels()},more stuff,${free_times()}\n")
tg.prod("skill_levels", lambda: next(skill_levels_generator))
tg.prod("free_times", lambda: next(free_times_adv_generator))
print(tg.gen("Classroom"))

