from makogram.grammar import Grammar
from makogram.parmgen import *
from random import gauss, triangular, choice, vonmisesvariate, uniform, sample
from statistics import mean
from math import ceil


## Parms
python_skill = Parm("python_skill", "normal", "many", "one-by-one", low=0, high=5, ave=3, dev=2)
java_skill = Parm("java_skill", "normal", "many", "one-by-one", low=0, high=5, ave=3, dev=2)
js_skill = Parm("js_skill", "normal", "many", "one-by-one", low=0, high=5, ave=3, dev=2)
c_skill = Parm("c_skill", "normal", "many", "one-by-one", low=0, high=5, ave=3, dev=2)
cpp_skill = Parm("cpp_skill", "normal", "many", "one-by-one", low=0, high=5, ave=3, dev=2)
php_skill = Parm("php_skill", "normal", "many", "one-by-one", low=0, high=5, ave=3, dev=2)
html_skill = Parm("html_skill", "normal", "many", "one-by-one", low=0, high=5, ave=3, dev=2)
sql_skill = Parm("sql_skill", "normal", "many", "one-by-one", low=0, high=5, ave=3, dev=2)
bashunix_skill = Parm("bashunix_skill", "normal", "many", "one-by-one", low=0, high=5, ave=3, dev=2)
available_times = Parm("available free times", "normal", "many", "fixed-size-chunks", low=0, high=19, ave=9, dev=6, from_set=days_of_week(), per_row=5)

python_skill.setup()
python_skill.scramble()
java_skill.setup()
java_skill.scramble()
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

def namelist(li):
        for thing in li:
                yield thing
n = namelist(names())


tg = Grammar()
tg.prod("Classroom", "${Student()}", reps=many(MAX_GENS)) #reps should be class_size
tg.prod("Student", "${name()},${python_skill()},${java_skill()},${js_skill()},${c_skill()},${cpp_skill()},${php_skill()},${html_skill()},${sql_skill()},${bashunix_skill()},${free_times()}\n")
tg.prod("name", lambda: next(n))
tg.prod("python_skill", lambda: python_skill.next())
tg.prod("java_skill", lambda: java_skill.next())
tg.prod("js_skill", lambda: js_skill.next())
tg.prod("c_skill", lambda: c_skill.next())
tg.prod("cpp_skill", lambda: cpp_skill.next())
tg.prod("php_skill", lambda: php_skill.next())
tg.prod("html_skill", lambda: html_skill.next())
tg.prod("sql_skill", lambda: sql_skill.next())
tg.prod("bashunix_skill", lambda: bashunix_skill.next())
tg.prod("free_times", lambda: available_times.next())
print(tg.gen("Classroom"))
