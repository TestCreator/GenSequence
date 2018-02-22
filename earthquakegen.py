from makogram.grammar import Grammar
from makogram.parmgen import *
from random import gauss, triangular, choice, vonmisesvariate, uniform, sample
from statistics import mean
from math import ceil
import csv

## Parms
magnitudes = Parm("magnitudes", "one-by-one", low=0.0, high=10.0, ave=3.3, dev=1.1)
latitudes = Parm("latitudes", "one-by-one", low=42.2197, high=49.4817, ave=45.84, dev=1.3)
longitudes = Parm("longitudes", "one-by-one", low=-124.8865, high=-119.1502, ave=-122.0184, dev=1.2)
depths = Parm("depths", "one-by-one", low=0.0, high=30.0, ave=15.0, dev=5.0)

def establish_magnitudes(disttype, des):
        magnitudes.setDistributionType(disttype)
        magnitudes.setDesired(des)
def establish_latitudes(disttype, des):
        latitudes.setDistributionType(disttype)
        latitudes.setDesired(des)
def establish_longitudes(disttype, des):
        longitudes.setDistributionType(disttype)
        longitudes.setDesired(des)
def establish_depths(disttype, des):
        depths.setDistributionType(disttype)
        depths.setDesired(des)


def regenerate_parm_data_points():
        magnitudes.setup()
        magnitudes.scramble()
        latitudes.setup()
        latitudes.scramble()
        longitudes.setup()
        longitudes.scramble()
        depths.setup()
        depths.scramble()


def declare_grammar_production_rules(repetitions):
        """
        num_lines is a string, "many" or "few" or "single" describing how many lines of data should be in the csv file
        gets passed into the reps argument of a grammar production rule
        the string is a proportion of MAX_GENS, a calibration point
        """
        tg = Grammar()
        tg.prod("Recordings", "${Event()}", reps=repetitions) #reps should be class_size
        tg.prod("Event", "${EventId()},${Magnitude()},${Epoch},${Time},${TimeLocal},${Distance},${Latitude()},${Longitude()},${DepthKm()},${DepthMi()}\n")
        tg.prod("EventId": lambda: random.randint(10000000, 70000000)) #TODO, specify in prm file?
        tg.prod("Magnitude", lambda: magnitudes.next())
        tg.prod("Epoch", "#####")
        tg.prod("Time", "12:00.0")
        tg.prod("TimeLocal", "2012/09/22 09:46:45 PDT") #TODO, randomize date time choice?
        tg.prod("Distance", "30.0 km (  18.6 mi) WSW ( 240. azimuth) from Millican, OR") #TODO, randomize choice?
        tg.prod("Latitude", lambda: latitudes.next())
        tg.prod("Longitude", lambda: longitudes.next())
        tg.prod("DepthKm", lambda: depths.next())
        tg.prod("DepthMi", lamdba: 100) #TODO - this is critical! static data point conversion

        return tg

if __name__=="__main__":
        testcount = 0
        with open("earthquakegentestvectors.csv", newline='') as vectorfile:
                reader = csv.DictReader(vectorfile)
                #iterate through all vectors
                for vector in reader:
                        testcount += 1
                        #set all parms
                        num_lines = translate_desired(vector['recordings']) #this is used for desired number in all parms
                        if num_lines == None:
                                break

                        establish_magnitudes(vector['magnitudes'], num_lines)
                        establish_latitudes(vector['latitudes'], num_lines)
                        establish_longitudes(vector['longitudes'], num_lines)
                        establish_depths(vector['depths'], num_lines)


                        #create new data sets
                        regenerate_parm_data_points()

                        #prepare the data file and file name
                        test_case_file_name = "cases/{}-{}-".format(testcount, num_lines)
                        for parm in ["magnitudes", "latitudes", "longitudes", "depths"]:
                                test_case_file_name += parm.split("_")[0] + ':' + vector[parm] + '-'

                        #generate new grammar
                        new_grammar = declare_grammar_production_rules(num_lines)
                        new_data = new_grammar.gen("Recordings").split('\n')

                        #and dump into concrete data file
                        with open("{}.csv".format(test_case_file_name), 'w', newline='') as concretefile:
                                fieldnames = ["EventId","Magnitude","Epoch","Time","TimeLocal","Distance","Latitude","Longitude","DepthKm","DepthMi"]
                                writer = csv.DictWriter(concretefile, fieldnames=fieldnames)
                                writer.writeheader()
                                for line in new_data:
                                        row = dict(zip(fieldnames, line.split(',', maxsplit=(len(fieldnames)-1))))
                                        writer.writerow(row)
                        print("[Log>: file #{:>2} complete, available for testing use".format(testcount, test_case_file_name))

