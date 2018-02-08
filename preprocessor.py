import sys

def get_file_name():
        syntax_file_to_read = ""
        for parm in sys.argv:
                if parm.endswith(".prm"):
                        syntax_file_to_read = parm
        return syntax_file_to_read

def open_and_print(filename):
        f = open(filename, 'r')
        stuff = f.read()
        print(stuff)
        f.close()

def main():
        open_and_print(get_file_name())

if __name__=="__main__":
        main()