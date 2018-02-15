import sys #to get command line args - the file name we want to compile!
from range import Range #Range objects are declared, often as globals
import ast #evaluation of strs into the objects the string represents

def eval_global(strrep):
        partition = strrep.split(' ') #['MAX_GENS', '100']
        rejoin = partition[0] + "=" + partition[1] #'MAX_GENS=100'
        tree = ast.parse(rejoin)
        compilable = compile(tree, filename='<string>', mode="exec")
        return res


def get_file_name():
        syntax_file_to_read = ""
        for parm in sys.argv:
                if parm.endswith(".prm"):
                        syntax_file_to_read = parm
        return syntax_file_to_read

def scrub_down(sectionalist):
        clean_section = []
        for lin in sectionalist:
                if (lin == "\n" or lin.startswith("#")):
                        continue
                ## get rid of comments, and then get rid of ending newline, and tabins. some tabins are read as multiple spaces
                lin = lin.split("#")[0].strip("\t").strip("\n").strip(' ') 
                clean_section.append(lin)
        return clean_section


def open_and_print(filename):
        f_in = open(filename, 'r') 

        # the parsing begins
        ############################

        sections = [[] for _ in range(10)]
        i = 0
        line = f_in.readline()
        while (line != ''):
                if (not line.startswith("%%%%%%%%%%%%%%%%%%%%")):
                        sections[i].append(line)
                else:
                        i += 1
                line = f_in.readline()

        for i in range(len(sections)):
                sections[i] = scrub_down(sections[i])
        for section in sections:
                print(section)
        for declaration in sections[0]:
                declare = eval_global(declaration)
                print(thingy)


        ############################
        f_in.close()

def main():
        open_and_print(get_file_name())

if __name__=="__main__":
        main()