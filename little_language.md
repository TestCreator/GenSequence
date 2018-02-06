#Comments
"#" are comments

#Globals
Globals are declared first, and of form <Symbol Name> <Value>
Value can be any type, but the type will be inferred
100 -> int, 100.0 -> float, or specialty objects (Range)

**************TODO
when declaring globals, particularly from_sets, should they be python-programatically defined or symbolic?
ex: (M, T, W, R, F)*(10:00-12:00, 12:00-2:00, 2:00-4:00, 4:00-6:00)
OR
[str(day + time) for day in ["M", "T", "W", "R", "F"] for time in ["10:00 - 12:00", "12:00 - 2:00", "2:00 - 4:00", "4:00 - 6:00"]]
***************

#Dimensions
@Horizontal and @Vertical begin to describe the columns and rows of the test case
@Horizontal will describe the number of rows, and the parameter can be named something
@Vertical is all the columns: Parameter Objects and their names

#General Rules
Syntax imitates Grammar Production Rules
X -> A | B turns into
X:
        A
        B

When declaring what "X" could be, the type must be described, ex:
X:
        int A
        int B

Note that "type" is a type, and implies the use of a distribution type, i.e. normal, uniform, etc.

@Vertical must always be made of col or multicol objects. col will become a Parm object, and multicol will become a Cardioid object.
multicols that are dependent on each have a later subsection that describes their relationship. Each singular multicol must be created
first and the joint distribution is enforced later, using a hillclimbing approach.

#Hillclimbing
A hillclimbing approach is used to enforce distributions between multicols. So arguments must be supplied to identify more favorable
changes.
parm1 "<<" parm2 denotes that parm2 has a dependency on parm1. A function must be supplied to combine cols in the multicol. Then 
relational properties are described using "->". 
