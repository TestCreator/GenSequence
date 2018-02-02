import random
from makogram.grammar import Grammar
from makogram.parmgen import *
from statistics import mean
from math import ceil
import csv
from range import Range

def frequency(raw_data):
        new_raw = sorted(raw_data)
        new_raw.append('sentinel')
        count = 0
        for i in range(0, len(raw_data)-1):
            if new_raw[i + 1] == new_raw[i]:
                count += 1
            else: #majors[major + 1] != majors[major]
                count += 1
                print ("Value {} has count {}".format(new_raw[i], count))
                count = 0

def average(figures):
        """
        :figures -> a list or tuple of points you want to average
        """
        sum = 0
        for point in figures:
                sum += point
        return sum/(len(figures))

def within(pick, ranges):
        """
        :pick: a tuple, i.e. (1,4)
        :ranges: a list of range tuples, i.e. [(range(0,3), range(4,6)), (range(4,6), range(0,3))]
                or more likely, a list of Range tuples, i.e. [(Range(0.0,2.0), Range(3.4,5.6)), Range(1.3, 2.7), Range(3.9, 6.7))]
        returns true if pick[0] in range[i][0] and pick[1] in range[i][1]
        """
        isin = 0
        for guy in ranges:
                #print("guy is currently {}, about to check if {} is in guy".format(guy, pick))
                isin += (pick[0] in guy[0] and pick[1] in guy[1])
        return isin


def hillclimb(points, favorite, l_iterations=10000):
        l = 0
        while l < l_iterations:
                l += 1
                # pick random tuple in list
                i = random.randint(0, len(points)-1)
                j = random.randint(0, len(points)-1)
                pick1 = points[i] #these points are a tuple of tuples - point sets from each multicol
                pick2 = points[j]
                #points[i][0] is point from languages
                #points[i][1] is point from nicheskills
                ave00 = average(pick1[0])
                ave01 = average(pick1[1])
                ave10 = average(pick2[0])
                ave11 = average(pick2[1])

                swap1 = (ave00, ave11)
                swap2 = (ave10, ave01)

                #if pairs of averages between multicols are of form (1,3) & (0,3)
                #       example: ((0,2),(2,4)) and ((0,0),(1,5)) gives averages of (1,3) and (0,3)
                #       swapping won't help
                if ave00 == ave10 or ave01 == ave11:
                        continue

                #if of the same type, LH LH or HL HL, no swap


                if within(swap2, favorite) and within(swap2, favorite):
                        print("bang!")
                        points[i] = (pick1[0], pick2[1])
                        points[j] = (pick2[0], pick1[1])
                        print("\tOriginally {} and {}, swapped to points[i] is {} and points[j] is {}".format((pick1[0], pick1[1]), (pick2[0], pick2[1]), points[i], points[j]))

        return points

def basic_hillclimb(points, favorite, l_iterations=10000):
        l = 0
        while (l < l_iterations):
                l+=1
                # pick random tuple in list
                i = random.randint(0, len(points)-1)
                j = random.randint(0, len(points)-1)
                pick1 = points[i] #these points are a tuple of tuples - point sets from each multicol
                pick2 = points[j]
                #if (1,5) and (0,5) or (0,4) and (2,4), swapping doesn't make sense
                if pick1[0] == pick2[0] or pick1[1] == pick2[1]:
                        continue

                #if both points are of the same form HL & HL, or LH & LH
                skip = False
                for x in range(len(favorite)):
                        if within(pick1, [favorite[x]]) and within(pick2, [favorite[x]]):
                                skip = True
                if skip:
                        continue
                ######


                new1 = (pick1[0], pick2[1])
                new2 = (pick2[0], pick1[1])
                #print("Originally {} and {}, swapped {} {}".format(pick1, pick2, new1, new2))
                if (within(new1, favorite)) and (within(new2, favorite)):
                        print("bang!")
                        points[i] = new1
                        points[j] = new2
                        print("\tOriginally {} and {}, swapped to points[i] is {} and points[j] is {}".format(pick1, pick2, points[i], points[j]))
                
        return points

pythonjava_skill = Cardioid("pythonjava_skill", "one-by-one", from_set=[c for c in "LMH"])
pythonjava_skill.setup()
languages = pythonjava_skill.getFinalDataSet()
print(languages)

sqlbash_skill = Cardioid("sqlbash_skill", "one-by-one", from_set=[c for c in "LMH"])
sqlbash_skill.setup()
nicheskills = sqlbash_skill.getFinalDataSet()
print(nicheskills)

Laverage = Range(0.0, 2.6) # -> [0.0, 2.6]
Maverage = Range(2.6, 3.7, exclusive_lower=True, exclusive_upper=True) # -> (2.6, 3.7)
Haverage = Range(3.7, 5) # -> [3.7, 5]
multi_column_favorites = [(Laverage, Laverage), (Laverage, Haverage), (Maverage, Laverage), (Maverage, Haverage)]
thing = list(zip(languages, nicheskills))  #TODO define an __iter__ method for Parms and Cardioids!
print("BREAKDOWN ---- ")
print(thing)
print(thing[0])
#newstuff = hillclimb(zip(pythonjava_skill, sqlbash_skill), multi_column_favorites)


"""
newstuff = hillclimb(stuff, [(range(0,3),range(4,6)), (range(4,6),range(0,3))], l_iterations=100000)
print(newstuff)

print ("\nBreakdown ------ ")
frequency(stuff)
print()
frequency(newstuff)
"""


