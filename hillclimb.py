import random
from makogram.grammar import Grammar
from makogram.parmgen import *
from statistics import mean
from math import ceil
import csv

def within(pick, ranges):
        """
        :pick: a tuple
        :range: a list of range tuples, i.e. [(range(0,3), range(4,6)), (range(4,6), range(0,3))]
        returns true if pick[0] in range[i][0] and pick[1] in range[i][1]
        """
        isin = 0
        for guy in ranges:
                isin += (pick[0] in guy[0] and pick[1] in guy[1])
        if isin > 1:
                return isin


def hillclimb(points, favorite):
        l = 0
        while l < 10000:
                # pick random tuple in list
                i = random.randint(0, len(points)-1)
                j = random.randint(0, len(points)-1)
                pick1 = points[i]
                pick2 = points[j]
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
newstuff = hillclimb(stuff, [(range(0,3),range(4,6)), (range(4,6),range(0,3))])
print(newstuff)