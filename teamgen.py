from makogram.grammar import Grammar
from makogram.parmgen import *
from random import gauss, triangular, choice, vonmisesvariate, uniform, sample
from statistics import mean
from math import ceil
import csv

#Ignore these for now
SKILLS_LIST = ['pythonjava_skill', 'js_skill', 'c_skill', 'cpp_skill', 'php_skill', 'html_skill', 'sql_skill', 'bashunix_skill']
#PARMS_LIST = [0 for _ in range(20)] #[python_skill, java_skill, js_skill, c_skill, cpp_skill, php_skill, html_skill, sql_skill, bashunix_skill, free_times]


## Parms
pythonjava_skill = Cardioid("pythonjava_skill", "one-by-one", from_set=[c for c in "LMH"])
js_skill = Parm("js_skill", "one-by-one", low=0, high=5, ave=3, dev=2)
c_skill = Parm("c_skill", "one-by-one", low=0, high=5, ave=3, dev=2)
cpp_skill = Parm("cpp_skill", "one-by-one", "normal", "many", low=0, high=5, ave=3, dev=2)
php_skill = Parm("php_skill", "one-by-one", low=0, high=5, ave=3, dev=2)
html_skill = Parm("html_skill", "one-by-one", low=0, high=5, ave=3, dev=2)
sql_skill = Parm("sql_skill", "one-by-one", low=0, high=5, ave=3, dev=2)
bashunix_skill = Parm("bashunix_skill", "one-by-one", low=0, high=5, ave=3, dev=2)

available_times = Parm("available free times", "fixed-size-chunks", low=0, high=19, ave=9, dev=6, from_set=days_of_week(), per_row=5)

n = names_generator(names())

def establish_js_skill(disttype, des):
        js_skill.setDistributionType(disttype)
        js_skill.setDesired(des)
def establish_c_skill(disttype, des):
        c_skill.setDistributionType(disttype)
        c_skill.setDesired(des)
def establish_cpp_skill(disttype, des):
        cpp_skill.setDistributionType(disttype)
        cpp_skill.setDesired(des)
def establish_php_skill(disttype, des):
        php_skill.setDistributionType(disttype)
        php_skill.setDesired(des)
def establish_html_skill(disttype, des):
        html_skill.setDistributionType(disttype)
        html_skill.setDesired(des)
def establish_sql_skill(disttype, des):
        sql_skill.setDistributionType(disttype)
        sql_skill.setDesired(des)
def establish_bashunix_skill(disttype, des):
        bashunix_skill.setDistributionType(disttype)
        bashunix_skill.setDesired(des)
def establish_available_times(disttype, des):
        available_times.setDistributionType(disttype)
        available_times.setDesired(des)
def regenerate_parm_data_points():
        pythonjava_skill.setup()
        pythonjava_skill.scramble()
        js_skill.setup()
        js_skill.scramble()
        c_skill.setup()
        c_skill.scramble()
        cpp_skill.setup()
        cpp_skill.scramble()
        php_skill.setup()
        php_skill.scramble()
        html_skill.setup()
        html_skill.scramble()
        sql_skill.setup()
        sql_skill.scramble()
        bashunix_skill.setup()
        bashunix_skill.scramble()
        available_times.setup()
        available_times.scramble()
        n = names_generator(names())



#guy = available_times.next()
#thing = sort_by_days(guy)
#print("got res: {}".format(thing))

def declare_grammar_production_rules(repetitions):
        """
        num_lines is a string, "many" or "few" or "single" describing how many lines of data should be in the csv file
        gets passed into the reps argument of a grammar production rule
        the string is a proportion of MAX_GENS, a calibration point
        """
        tg = Grammar()
        tg.prod("Classroom", "${Student()}", reps=repetitions) #reps should be class_size
        tg.prod("Student", "${timestamp},${name()},${duckid},${pythonjava_skill()},${js_skill()},${c_skill()},${cpp_skill()},${php_skill()},${html_skill()},${sql_skill()},${bashunix_skill()},${free_times()}\n")
        tg.prod("timestamp", "12:00.0")
        tg.prod("name", lambda: next(n))
        tg.prod("duckid", "placeholder")
        tg.prod("pythonjava_skill", lambda: pythonjava_skill.next())
        tg.prod("js_skill", lambda: js_skill.next())
        tg.prod("c_skill", lambda: c_skill.next())
        tg.prod("cpp_skill", lambda: cpp_skill.next())
        tg.prod("php_skill", lambda: php_skill.next())
        tg.prod("html_skill", lambda: html_skill.next())
        tg.prod("sql_skill", lambda: sql_skill.next())
        tg.prod("bashunix_skill", lambda: bashunix_skill.next())
        tg.prod("free_times", lambda: sort_by_days(available_times.next()))

        return tg

if __name__=="__main__":
        testcount = 0
        with open("teamgentestvectors.csv", newline='') as vectorfile:
                reader = csv.DictReader(vectorfile)
                #iterate through all vectors
                for vector in reader:
                        testcount += 1
                        #set all parms
                        num_lines = translate_desired(vector['class_size']) #this is used for desired number in all parms
                        if num_lines == None:
                                break

                        establish_js_skill(vector['js_skill'], num_lines)
                        establish_c_skill(vector['c_skill'], num_lines)
                        establish_cpp_skill(vector['cpp_skill'], num_lines)
                        establish_php_skill(vector['php_skill'], num_lines)
                        establish_html_skill(vector['html_skill'], num_lines)
                        establish_sql_skill(vector['sql_skill'], num_lines)
                        establish_bashunix_skill(vector['bashunix_skill'], num_lines)
                        establish_available_times(vector['free_times'], num_lines)

                        #create new data sets
                        regenerate_parm_data_points()

                        #prepare the data file and file name
                        test_case_file_name = "cases/{}-{}-".format(testcount, num_lines)
                        for skill in SKILLS_LIST+['free_times']:
                                test_case_file_name += skill.split("_")[0] + ':' + vector[skill] + '-'

                        #generate new grammar
                        new_grammar = declare_grammar_production_rules(num_lines)
                        new_data = new_grammar.gen("Classroom").split('\n')

                        #and dump into concrete data file
                        with open("{}.csv".format(test_case_file_name), 'w', newline='') as concretefile:
                                fieldnames = ['Timestamp', 'Student Name', 'Your Duck Id'] + SKILLS_LIST + ['available_times']
                                writer = csv.DictWriter(concretefile, fieldnames=fieldnames)
                                writer.writeheader()
                                for line in new_data:
                                        row = dict(zip(fieldnames, line.split(',', maxsplit=(len(fieldnames)-1))))
                                        writer.writerow(row)
                        print("[Log>: file #{:>2} complete, available for testing use".format(testcount, test_case_file_name))

