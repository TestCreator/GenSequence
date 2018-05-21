from makogram.grammar import Grammar
from makogram.parmgen import *
from makogram.vectorparm import *
from makogram.range import Range
from makogram.cardioid import Cardioid
from random import gauss, triangular, choice, vonmisesvariate, uniform, sample, randint
from statistics import mean
import csv


## Ranges
smallmass = Range(1.314E+22, 2.96E+26)
largemass = Range(2.96E+27, 1.9891E+30)

andromeda_x = Range(-4.55E+12, -4.55E+10)
andromeda_y = Range(-3.89E+12, -3.89E+10)
andromeda_z = Range(-5.79E+10, -5.79E+8)

pinwheel_x = Range(1.08E+4, 1.08E+8)
pinwheel_y = Range(8.51E+3, 8.51E+7)
pinwheel_z = Range(1.28E+4, 1.28E+8)

lowspeed_x = Range(-100.0, 100.0)
lowspeed_y = Range(-1000.0, 1000.0)
lowspeed_z = Range(-100.0, 100.0)

halfspeed_x = Range(-6487.118, -5000.0)
halfspeed_y = Range(-11417.83, -8000.0)
halfspeed_z = Range(-2031.506, -1000.0)

smalldiam = Range(0.0, 2.4)
largediam = Range(5.5, 7.0)


## Parms
mass = Parm("mass", "one-by-one", low=1.314E+22, high=1.9891E+30, ave=2.96E+26, dev=3.09E+25)

position = VectorParm("position", "one-by-one", from_set=[Range(-4.55E+12, 1.08E+12), Range(-3.89E+12, 8.51E+11), Range(-5.79E+10, 1.28E+12)])
position.setFavorites([(andromeda_x, andromeda_y, andromeda_z)])
position.setNonFavorites([(pinwheel_x, pinwheel_y, pinwheel_z)])

velocity = VectorParm("velocity", "one-by-one", from_set=[Range(-6487.118, 635.998), Range(-11417.83, 41093.05), Range(-2031.506, 6918.461)])
velocity.setFavorites([(lowspeed_x, lowspeed_y, lowspeed_z)])
velocity.setNonFavorites([(halfspeed_x, halfspeed_y, halfspeed_z)])

diameter = Parm("diameter", "one-by-one", low=2.0, high=7.0, ave=4.66667, dev=1.1)
diameter.setFavorites([smalldiam])
diameter.setNonFavorites([largediam])


massvelofavs = [(smallmass, (lowspeed_x, lowspeed_y, lowspeed_z)), #List[Tuple(Range, Tuple(Range, Range, Range))]
                (largemass, (halfspeed_x, halfspeed_y, halfspeed_z))
                ] 
massvelooutliers = [(smallmass, (halfspeed_x, halfspeed_y, halfspeed_z)),
                    (largemass, (lowspeed_x, lowspeed_y, lowspeed_z))
                    ]
massvelo = Cardioid(mass, velocity)
massvelo.setFavorites(massvelofavs)
massvelo.setNonFavorites(massvelooutliers)



def establish_mass(disttype, des):
        massvelo.firstParm.setDistributionType(disttype)
        massvelo.firstParm.setDesired(des)
def establish_position(disttype, des):
        position.setDistributionType(disttype)
        position.setDesired(des)
def establish_velocity(disttype, des):
        massvelo.secondParm.setDistributionType(disttype)
        massvelo.secondParm.setDesired(des)
def establish_diameter(disttype, des):
        diameter.setDistributionType(disttype)
        diameter.setDesired(des)


def regenerate_parm_data_points():
        massvelo.generate() #rewrites final data sets for both parms
        position.setup()
        position.scramble()
        diameter.setup()
        diameter.scramble()

def scrub_data(in_data, remove):
        """
        in_data - List of strings
        remove - string of chars to remove from each string in each list

        cleans up randomly floating around characters 
        """
        for i in range(len(in_data)):
                record = in_data[i].split(",")
                for j in range(len(record)):
                        record[j] = record[j].strip(remove)
                in_data[i] = ",".join(record)
        while in_data.remove("") != None:
                continue

def create_field_names(*args):
        """ a variable amount of objects passed in -- only Strings, Parms and VectorParms! No Cardioid """
        headers = []
        for parm in args:
                if isinstance(parm, VectorParm):
                        for i in range(parm.per_row):
                                column_name = "{}_{}".format(parm.name, (i+1))
                                headers.append(column_name)
                        continue
                elif isinstance(parm, Parm):
                        headers.append(parm.name)
                else:
                        headers.append(parm)
        return headers


def declare_grammar_production_rules(repetitions):
        """
        num_lines is a string, "many" or "few" or "single" describing how many lines of data should be in the csv file
        gets passed into the reps argument of a grammar production rule
        the string is a proportion of MAX_GENS, a calibration point
        """
        og = Grammar()
        og.prod("Planets", "${Planet()}", reps=repetitions) #reps should be class_size
        og.prod("Planet", "${Name()},${Mass()},${Position()},${Velocity()},${Diameter()},${Color}\n")
        og.prod("Name", "body") #TODO, specify in prm file?
        og.prod("Mass", lambda: massvelo.firstParm.next())
        og.prod("Position", lambda: position.next())
        og.prod("Velocity", lambda: massvelo.secondParm.next())
        og.prod("Diameter", lambda: diameter.next())
        og.prod("Color", "#ffffbf") #TODO - colorize different every row
        return og

if __name__=="__main__":
        testcount = 0
        with open("orbitsgentestvectors.csv", newline='') as vectorfile:
                reader = csv.DictReader(vectorfile)
                #iterate through all vectors
                for vector in reader:
                        testcount += 1
                        #set all parms
                        num_lines = translate_desired(vector['Planets']) #this is used for desired number in all parms
                        if num_lines == None:
                                break

                        establish_mass(vector['mass'], num_lines)
                        establish_position(vector['position'], num_lines)
                        establish_velocity(vector['velocity'], num_lines)
                        establish_diameter(vector['diameter'], num_lines)

                        #create new data sets
                        regenerate_parm_data_points()

                        #prepare the data file and file name
                        test_case_file_name = "cases2/{}-{}-".format(testcount, num_lines)
                        for parm in ["mass", "position", "velocity", "diameter"]:
                                test_case_file_name += parm.split("_")[0] + '|' + vector[parm] + '-'

                        #generate new grammar
                        new_grammar = declare_grammar_production_rules(num_lines)
                        new_data = new_grammar.gen("Planets").split('\n')

                        scrub_data(new_data, '()"')
                        #print(new_data)
                        #and dump into concrete data file
                        with open("{}.csv".format(test_case_file_name), 'w', newline='') as concretefile:
                                new_fieldnames = create_field_names("#Name", mass, position, velocity, diameter, "Color")
                                writer = csv.DictWriter(concretefile, fieldnames=new_fieldnames)
                                writer.writeheader()
                                for line in new_data:
                                        row = dict(zip(new_fieldnames, line.split(',', maxsplit=(len(new_fieldnames)-1))))
                                        writer.writerow(row)
                        print("[Log>: file #{:>2} complete, available for testing use".format(testcount, test_case_file_name))
                        
