from makogram.grammar import Grammar
from makogram.parmgen import *
from makogram.cardioid import Cardioid
from random import gauss, triangular, choice, vonmisesvariate, uniform, sample, randint
from statistics import mean
from math import ceil
import csv

MAX_GENS = 100

def map_desired(ident):
        try:
                x = int(ident)
                return x
        except ValueError as e:
                if ident == "many":
                        return int(.7 * MAX_GENS)
                if ident == "few":
                        return int(.3 * MAX_GENS)
        return MAX_GENS


#magnitudes ranges
TotalMags = Range(0.0, 10.0, exclusive_upper=True, ave=3.3, dev=1.1)
Micro = Range(0.0, 2.0, exclusive_upper=True)
Feelable = Range(4.5, 7.9, exclusive_lower=True)
Great = Range(8.0, 9.5, exclusive_lower=True, exclusive_upper=True)

#depths ranges
TotalDepths = Range(0.0, 30.0, exclusive_upper=True, ave=15.0, dev=5.0)
Shallow = Range(0.0, 5.0, exclusive_lower=True, exclusive_upper=True)
Mid = Range(5.0, 15.0)
Deep = Range(15.0, 30.0, exclusive_lower=True)

#latitudes ranges
TotalLats = Range(38.58, 51.23, exclusive_lower=True, exclusive_upper=True, ave=44.9, dev=1.8)
East = Range(45.0, 51.23, exclusive_lower=True, exclusive_upper=True)
West = Range(38.58, 44.0, exclusive_lower=True, exclusive_upper=True)

#longitudes ranges
TotalLongs = Range(-128.6085, -114.0844, exclusive_lower=True, exclusive_upper=True, ave=-121.347, dev=2.2)
North = Range(-128.3444, -121.0184, exclusive_lower=True, exclusive_upper=True)
South = Range(-122.0184, -114.0333, exclusive_lower=True, exclusive_upper=True)

## Parms
Mags = Parm("magnitudes", "one-by-one", TotalMags)
Lats = Parm("latitudes", "one-by-one", TotalLats)
Longs = Parm("longitudes", "one-by-one", TotalLongs)
Depths = Parm("depths", "one-by-one", TotalDepths)

MagsDepths = Cardioid(Mags, Depths)
LatsLongs = Cardioid(Lats, Longs)


#Cardioid cardioid
MagsDepths.setFavorites([(Micro,Shallow), (Great,Deep), (Feelable,Mid)])
MagsDepths.setNonFavorites([(Micro,Deep), (Great,Shallow), (Feelable,Deep), (Feelable,Shallow)])

LatsLongs.setFavorites([(North,East)])
LatsLongs.setNonFavorites([(South,West)])

#Parm _cardioid
Mags.setFavorites(Micro)
Mags.setNonFavorites(Great)

Depths.setFavorites(Shallow)
Depths.setNonFavorites(Deep)

Lats.setFavorites(East)
Lats.setNonFavorites(West)

Longs.setFavorites(North)
Longs.setNonFavorites(South) 



def establish_Mags(disttype, des):
        MagsDepths.firstParm.setDistributionType(disttype)
        MagsDepths.firstParm.setDesired(des)
def establish_Lats(disttype, des):
        LatsLongs.firstParm.setDistributionType(disttype)
        LatsLongs.firstParm.setDesired(des)
def establish_Longs(disttype, des):
        LatsLongs.secondParm.setDistributionType(disttype)
        LatsLongs.secondParm.setDesired(des)
def establish_Depths(disttype, des):
        MagsDepths.secondParm.setDistributionType(disttype)
        MagsDepths.secondParm.setDesired(des)


def regenerate_parm_data_points():
        MagsDepths.generate() #rewrites final data sets for both parms
        LatsLongs.generate()


def declare_grammar_production_rules(repetitions):
        """
        num_lines is a string, "many" or "few" or "single" describing how many lines of data should be in the csv file
        gets passed into the reps argument of a grammar production rule
        the string is a proportion of MAX_GENS, a calibration point
        """
        tg = Grammar()
        tg.prod("Recordings", "${Event()}", reps=repetitions) #reps should be class_size
        tg.prod("Event", "${EventId()},${Magnitude()},${Epoch},${Time},${TimeLocal},${Distance},${Latitude()},${Longitude()},${DepthKm()},${DepthMi()}\n")
        tg.prod("EventId", lambda: randint(10000000, 70000000)) #TODO, specify in prm file?
        tg.prod("Magnitude", lambda: MagsDepths.firstParm.next())
        tg.prod("Epoch", "#####")
        tg.prod("Time", "12:00.0")
        tg.prod("TimeLocal", "2012/09/22 09:46:45 PDT") #TODO, randomize date time choice?
        tg.prod("Distance", "30.0 km (  18.6 mi) WSW ( 240. azimuth) from Millican OR") #TODO, randomize choice?
        tg.prod("Latitude", lambda: LatsLongs.firstParm.next())
        tg.prod("Longitude", lambda: LatsLongs.secondParm.next())
        tg.prod("DepthKm", lambda: MagsDepths.secondParm.next())
        tg.prod("DepthMi", "100") #TODO - this is critical! static data point conversion
        return tg

if __name__=="__main__":
        testcount = 0
        with open("earthquakegentestvectors.csv", newline='') as vectorfile:
                reader = csv.DictReader(vectorfile)
                #iterate through all vectors
                for vector in reader:
                        testcount += 1
                        #set all parms
                        num_lines = map_desired(vector['Recordings']) #this is used for desired number in all parms
                        if num_lines == None:
                                break

                        establish_Mags(vector['Mags'], num_lines)
                        establish_Lats(vector['Lats'], num_lines)
                        establish_Longs(vector['Longs'], num_lines)
                        establish_Depths(vector['Depths'], num_lines)


                        #create new data sets
                        regenerate_parm_data_points()

                        #prepare the data file and file name
                        test_case_file_name = "cases1/{}-{}-".format(testcount, num_lines)
                        for parm in ["Mags", "Lats", "Longs", "Depths"]:
                                test_case_file_name += parm.split("_")[0] + ':' + vector[parm] + '-'
                        #generate new grammar
                        new_grammar = declare_grammar_production_rules(num_lines)
                        new_data = new_grammar.gen("Recordings").split("\n")
                        new_data = new_data[0:len(new_data)-1]

                        #and dump into concrete data file
                        with open("{}.csv".format(test_case_file_name), 'w', newline='') as concretefile:
                                fieldnames = ["#EventId","Magnitude","Epoch","Time","TimeLocal","Distance","Latitude","Longitude","DepthKm","DepthMi"]
                                writer = csv.DictWriter(concretefile, fieldnames=fieldnames)
                                writer.writeheader()
                                for line in new_data:
                                        row = dict(zip(fieldnames, line.split(',', maxsplit=(len(fieldnames)-1))))
                                        writer.writerow(row)
                        print("[Log>: file #{:>2} complete, available for testing use".format(testcount, test_case_file_name))

