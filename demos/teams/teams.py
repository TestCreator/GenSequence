"""
Example test data generator for team formation. 

What can we factor out of this to be reused across 
applications? 

For this example, a test case consists of: 
   - A CSV file representing the class 
   - Parameters for the team builder: 
      - Desired team size
   So each test case is three files: 
    ## later ## - A test description (documentation)
    - A "test runner" program (shell script?), which 
      should include oracles  (how?)
    - A CSV file for the class 

2nd prototype: Can I use a grammar to capture some inter-record
patterns?  Things to control: 
   * Class size:  as 'max_uses' constraint
     exclusive of size of 'remnant' groups
   * Skills mix, time mix: 
     generate list as two or three sets of productions, of 
     different lengths: 
       - number of students with typical, random distribution 
         of free times.
       - number of students who can only meet in evenings, 
         number of students who can only meet in mornings
       - number of students who only know C++, number of 
         students who only know Java
Does grammar really help with this?  Maybe straightforward 
program control is better?
"""
import argparse
import csv
import sys
import arrow   # For timestamps in student questionnaire records
import random 

import context
from distribute import draw
from  makogram.grammar import Grammar

freetime_choices_mwf = ["9:00-12:00", "12:00-2:00", "2:00-4:00", "4:00-6:00"]
freetime_choices_uh = ["12:00-2:00", "2:00-4:00", "4:00-6:00"]

#
# Meeting time availability
# 
def some_times(from_list,min=1,max=3):
    return ";".join(draw.sample_ordered_m_n(from_list,min,max))

#
# Technology skills/experience
# We'll imagine that each student has at least one technical skill,
# up to five, with randomly distributed skill ranges 1-5; other
# skills are 0 (so zero has a different distribution from the other
# levels)
# 
# We'll generate skill levels as a vector, then separately load that
# into a dict.  There are 9 skills in the Flying Bison questionnaire.
#
def skill_levels():
    """
    Vector of skill levels 0-5
    """
    n_possible_skills = 9  # This would change if questionnaire schema changed
    skills = [0]*n_possible_skills         # Initially no skills
    n_skills = random.randint(1,5)
    for i in range(n_skills):
        skill_level = random.randint(1,5)
        # Which skill to update?  Choosing randomly means we may
        # have collisions, which somewhat reduce the overall skill
        # level.  I think that's fairly harmless given the arbitrariness
        # of my assumptions about skill levels.
        skill_to_update = random.randrange(n_possible_skills)
        skills[skill_to_update] = skill_level
    return skills

#
# Distribute vector elements to named elements of a dict.
# The name "scatter" derives from the scatter/gather idiom
# of I/O or message passing.
#
def scatter(vec, field_names, dest):
    """
    Values from vec are assigned to each corresponding field_name 
    in dictionary dest.  The lengths of vec and field_names must be 
    equal. 
    """
    assert len(vec) == len(field_names)
    for i in range(len(vec)):
        dest[field_names[i]] = vec[i]


## Field titles
#  Each field in the CSV file has a variable containing its
#  name.
timestamp = "Timestamp",
name =  "Student Name"
id = "Your DuckID"
exp_py =  "Python experience",
exp_jav =  "Java experience",
exp_js =  "Javascript experience",
exp_c =  "C experience",
exp_cpp =  "C++ experience",
exp_php =  "PHP experience",
exp_html =  "HTML experience",
exp_sql =  "SQL experience",
exp_bsh =  "Bash/Unix experience",
monday =  "Monday"
tuesday =  "Tuesday",
wednesday =  "Wednesday"
thursday =  "Thursday"
friday =  "Friday"
teammates =  "Desired Teammates DuckIDs (separated by ';')" 


fieldnames = [timestamp, name, id, exp_py, exp_jav, exp_js,
                  exp_c, exp_cpp, exp_php, exp_html, exp_sql,
                  exp_bsh, monday, tuesday, wednesday, thursday,
                  friday, teammates ]


def generate_tests(infile,outpath_prefix):
    """
    Generate a concrete test case for each test vector
    in infile.  
    """
    count = 0
    reader = csv.DictReader(infile)
    for test_vec in reader:
        generate_test(test_vec,outpath_prefix, "{}".format(count))
        count += 1


# Mapping value names to parameters used in generating
# concrete values
class_sizes = { "0": (0,0),  "1": (1,1), "2": (2,2),
                    "small": (8,18), "medium": (20,35),
                    "large": (40,80) }

def choose_class_size(test_vec):
    min, max = class_sizes[test_vec["class_size"]]
    if min==max:
        return min
    return random.randint(min,max)

# Not clear how team size would be set ... it is currently
# supplied through a GUI, and the test cases produced in
# spring 2017 do not include it.  I'll skip that for now. 
#

# Time overlaps.  How shall we interpret this?
# some_times draws the times; we'll fix it there
#

def generate_test(test_vec, outpath_prefix, outpath_suffix):
    """
    Generate one concrete test case based on the test vector. 
    outpath_prefix and outpath_suffix are parts of the file names
    to be generated; the suffix part gives uniqueness.
    """
    global names_source
    names_source=draw.full_names()
    runner_name = "{}{}_runner.sh".format(outpath_prefix, outpath_suffix)
    classfile_name = "{}{}_class.csv".format(outpath_prefix, outpath_suffix)
    with open(runner_name, 'w') as runner:
        print("#! env python3 myprog {} ".format(classfile_name),file=runner)
        print("# For test vector {}".format(test_vec), file=runner)
    # print("Test vector: {}".format(test_vec))
    with open(classfile_name, 'w') as classfile:
        writer = csv.DictWriter(classfile,fieldnames=fieldnames)
        writer.writeheader()
        for _ in range( choose_class_size(test_vec)):
            writer.writerow( gen_student_record(test_vec) )
        

#
# A vector of concrete values for a single row of the
# output test sequence.  Since this is a function and not
# a generator, and since we don't have other state maintenance
# mechanisms, we currently have no relations between rows.
#
def gen_student_record(test_vec):
    """One student record"""
    rec = {timestamp: arrow.now(),
           name: next(names_source).strip(),
           id: draw.rand_str(9,"0123456789"),
           teammates: ""}
    skills = skill_levels();
    scatter(skills, [exp_py, exp_jav, exp_js, exp_c,
                  exp_cpp, exp_php, exp_html, exp_sql,exp_bsh],
                  rec)
    
    rec[monday] = some_times(freetime_choices_mwf,0,4)
    rec[tuesday] = some_times(freetime_choices_uh, 0,3)
    rec[wednesday] = some_times(freetime_choices_mwf,0,4)
    rec[thursday] = some_times(freetime_choices_uh, 0,3)
    rec[friday] = some_times(freetime_choices_mwf,0,4)
    return rec



def get_cli_args():
    """
    Get arguments from Unix command line interface
    Returns namespace mapping options to values 
    """
    parser=argparse.ArgumentParser(description="Generate test data for team formation")
    parser.add_argument("input_csv", default=sys.stdin, 
                            type=argparse.FileType('r',encoding="utf-8",errors="replace"))
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    args = get_cli_args()
    generate_tests(args.input_csv, "generated/")
                        




    
    
