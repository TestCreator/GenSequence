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
"""
import argparse
import csv
import sys
import arrow   # For timestamps in student questionnaire records
import genseq  # Experimental support for random streams
import random 
import rand_util # Other selection that is not about streams

freetime_choices_mwf = ["9:00-12:00", "12:00-2:00", "2:00-4:00", "4:00-6:00"]
freetime_choices_uh = ["12:00-2:00", "2:00-4:00", "4:00-6:00"]

#
# Meeting time availability
# 
def some_times(from_list,min=1,max=3):
    return ";".join(rand_util.choose_ordered_m_n(from_list,min,max))

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

fieldnames = ["time", "name", "id",
                  "exp_py", "exp_jav", "exp_js", "exp_c",
                  "exp_cpp", "exp_php", "exp_htm", "exp_sql","exp_bsh",
                  "mon", "tue", "wed", "thu", "fri",
                  "mates"]
field_titles = { "time": "Timestamp",
                     "name": "Student Name"
                     "id","Your DuckID"
                     "exp_py": "Python experience",
                     "exp_jav": "Java experience",
                     "exp_js": "Javascript experience",
                     "exp_c": "C experience",
                     "exp_cpp": "C++ experience",
                     "exp_php": "PHP experience",
                     "exp_htm": "HTML experience",
                     "exp_sql": "SQL experience",
                     "exp_bsh": "Bash/Unix experience",
                     "mon": "Monday", "tue": "Tuesday",
                     "wed": "Wednesday", "thu": "Thursday", "fri": "Friday",
                     "mates": "Desired Teammates DuckIDs (separated by ';')" }


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


def generate_test(test_vec, outpath_prefix, outpath_suffix):
    """
    Generate one concrete test case based on the test vector. 
    outpath_prefix and outpath_suffix are parts of the file names
    to be generated; the suffix part gives uniqueness.
    """
    global names_source
    names_source=genseq.names()
    runner_name = "{}{}_runner.sh".format(outpath_prefix, outpath_suffix)
    classfile_name = "{}{}_class.csv".format(outpath_prefix, outpath_suffix)
    with open(runner_name, 'w') as runner:
        print("#! env python3 myprog {} ".format(classfile_name),file=runner)
        print("# For test vector {}".format(test_vec), file=runner)
    # print("Test vector: {}".format(test_vec))
    with open(classfile_name, 'w') as classfile:
        writer = csv.DictWriter(classfile,fieldnames=fieldnames)
        writer.writeheader()
        # First cut:  20 student records, ignore the test vector'
        # FIXME: Vary contents of test file based on test vector
        for _ in range( choose_class_size(test_vec)):
            writer.writerow( gen_student_record() )
        

#
# A vector of concrete values for a single row of the
# output test sequence.  Since this is a function and not
# a generator, and since we don't have other state maintenance
# mechanisms, we currently have no relations between rows.
#
def gen_student_record():
    """One student record"""
    rec = {"time": arrow.now(),
           "name": next(names_source),
           "id": rand_util.rand_str(9,"0123456789"),
           "mates": ""}
    skills = skill_levels();
    scatter(skills, ["exp_py", "exp_jav", "exp_js", "exp_c",
                  "exp_cpp", "exp_php", "exp_htm", "exp_sql","exp_bsh"],
                  rec)
    rec["mon"] = some_times(freetime_choices_mwf,0,4)
    rec["tue"] = some_times(freetime_choices_uh, 0,3)
    rec["wed"] = some_times(freetime_choices_mwf,0,4)
    rec["thu"] = some_times(freetime_choices_uh, 0,3)
    rec["fri"] = some_times(freetime_choices_mwf,0,4)
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
                        




    
    
