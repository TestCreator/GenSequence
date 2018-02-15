import random
import context
import re
from makogram.grammar import Grammar

from case import Case

def rand_str():
    return "unknown"
    #return ''.join(random.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(6))
def rand_place():
    return "city, state"
def rand_num():
    return random.uniform(0.0, 9.0)
def entrynumber():
    return random.randint(10000000, 90000000) #just some identity number


### Magnitude functions
def norm_magnitude():
    a = random.gauss(3.5, 2.6)
    while (0.0 <= a <= 10.0) == False:
        a = random.gauss(3, 4)
    return round(a, 1)

def uni_magnitude():
    return round(random.uniform(0.1, 10.0), 1)


### Latitude Longitude pairs
def uni_latitude():
    return random.uniform(42.2197, 49.4817);
def pre_latitude():
    return random.choice([random.uniform(42.2197, 44.5000), random.uniform(45.5000, 49.4817)])
def uni_longitude():
    return random.uniform(-124.8865, -119.1502)
def pre_longitude():
    return random.choice([random.uniform(-124.8865, -122.0000), random.uniform(-121.0000, -1191502)])

### Depth functions
def uni_depth():
    return round(random.uniform(0.0, 33.0), 2)
def pre_depth():
    return round(random.choice([random.uniform(0.0, 10.0), random.uniform(20.0, 33.0)]), 2)

case1 = Case("many", "uniform", "preclustered", "preclustered", "uniform")
#case2 = Case("few", "normal", "uniform", "uniform", "preclustered")
testsuite = [case1]

eg = Grammar()

#the oracles can and likely will become more complex
eg.add_oracle_possibility("Latitude", "normal", "clustering is split at center")
eg.add_oracle_possibility("Latitude", "uniform", "unknown")
eg.add_oracle_possibility("Latitude", "preclustered", "clustering should match the patterns already")
eg.add_oracle_possibility("Longitude", "normal", "clustering is split at center")
eg.add_oracle_possibility("Longitude", "uniform", "unknown")
eg.add_oracle_possibility("Longitude", "preclustered", "clustering should match the patterns already")
eg.add_oracle_possibility("Magnitude", "normal", "std deviation quite small")
eg.add_oracle_possibility("Magnitude", "uniform", "std deviation unpredictable")
eg.add_oracle_possibility("Magnitude", "preclustered", "std deviation skewed")
eg.add_oracle_possibility("Depth", "preclustered", "std deviation skewed, but each cluster should have low deviation")
eg.add_oracle_possibility("Depth", "uniform", "unknown - evenly distributed")


testinstance = 1;
oraclefilename = "oracles"
oraclefile = open(oraclefilename, "w")

for case in testsuite:
    if case.entries == "many":
        eg.prod("Lines", "${Entry()}", reps=200)
    elif case.entries == "few":
        eg.prod("Lines", "${Entry()}", reps=100)
    eg.prod("Entry", "${EntryNumber()},${Magnitude()},#########,${LocalTime()},${GlobalTime()},\"${RelativeLocation()}\",${Latitude()},${Longitude()},${Unknown()},${Depth()}\n")
    eg.prod("EntryNumber", entrynumber);
    
    #case.magnitudes is either "normal" or "uniform"
    eg.prod("Magnitude", norm_magnitude, type=case.magnitudes)
    eg.prod("LocalTime", rand_str);
    # eg.prod("GlobalTime", "${Date()} ${Time()} ${TimeZone()}") #### This one is ok to ignore for now
    eg.prod("GlobalTime", rand_str)
    eg.prod("RelativeLocation", rand_place);
    #case.latitude/longitude is "uniform" or "preclustered"
    eg.prod("Latitude", pre_latitude, type=case.latitude)
    eg.prod("Longitude", pre_longitude, type=case.longitude)
    eg.prod("Unknown", rand_num)
    eg.prod("Depth", uni_depth, case.depths)

    #Generate the concrete test case
    test = eg.gen("Lines")
    testfile = open(str(testinstance) + ".csv", "w")
    for line in test:
        testfile.write(line)
    #write the corresponding oracle hints to the oracle file
    oraclefile.write(str(testinstance) + ".csv has only some chance of having these qualities...\n")
    oraclefile.write("Parameter--\tPrediction--\n")
    for col,pred in eg.oracle.items():
        oraclefile.write(col + "\t" + pred + "\n")
        
    ## We need some way of flushing the production rules -- otherwise we have a Choice when we generate another test case
    testinstance += 1





'''
if __name__ == "__main__":
    case = eg.gen("Lines")
    print("The Oracle is:")
    print(case['oracle'])
    print("\nTest Data following...")
    fh = open("cases.csv", "w")
    for line in case["testsuite"]:
        fh.write(line)
    print(case["testsuite"])

'''




