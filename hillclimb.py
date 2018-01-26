import random
from makogram.grammar import Grammar
from makogram.parmgen import *
from statistics import mean
from math import ceil
import csv

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

def within(pick, ranges):
        """
        :pick: a tuple, i.e. (1,4)
        :ranges: a list of range tuples, i.e. [(range(0,3), range(4,6)), (range(4,6), range(0,3))]
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
                # pick random tuple in list
                i = random.randint(0, len(points)-1)
                j = random.randint(0, len(points)-1)
                pick1 = points[i]
                pick2 = points[j]

                #if (1,5) and (0,5) or (0,4) and (2,4), swapping doesn't make sense
                if pick1[0] == pick2[0] or pick1[1] == pick2[1]:
                        #don't need to increment for a failed swap
                        continue

                #if both points are of the same form HL & HL, or LH & LH
                skip = False
                for x in range(len(favorite)):
                        if within(pick1, [favorite[x]]) and within(pick2, [favorite[x]]):
                                skip = True
                if skip:
                        #don't need to increment for a failed step
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
                l += 1
        return points

pythonjava_skill = Cardioid("pythonjava_skill", "one-by-one", from_set=[c for c in "LMH"])
pythonjava_skill.setup()
stuff = pythonjava_skill.getFinalDataSet()
print(stuff)
#frequency(stuff)

newstuff = hillclimb(stuff, [(range(0,3),range(4,6)), (range(4,6),range(0,3))], l_iterations=100000)
print(newstuff)
#frequency(newstuff)


