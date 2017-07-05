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

def generate_test(test_vec, outpath_prefix, outpath_suffix):
    """
    Generate one concrete test case based on the test vector. 
    outpath_prefix and outpath_suffix are parts of the file names
    to be generated; the suffix part gives uniqueness.
    """
    runner_name = "{}{}_runner.sh".format(outpath_prefix, outpath_suffix)
    classfile_name = "{}{}_class.csv".format(outpath_prefix, outpath_suffix)
    with open(runner_name, 'w') as runner:
        print("#! env python3 myprog {} ".format(classfile_name))
    # print("Test vector: {}".format(test_vec))
    with open(classfile_name, 'w') as classfile:
        writer = csv.DictWriter(classfile,fieldnames=fieldnames)



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
                        




    
    
