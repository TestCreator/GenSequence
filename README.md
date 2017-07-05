#GenSequence

From a CSV file representing a sequence of test vectors, produce a set of sequences of concrete values, one sequence per test vector.  Intended to be used in creation of concrete test cases as a step in a pipeline after GenPairs. 

## Status
Work in progress.  Currently small, partial prototypes to explore approaches. 

## Open Issues

### Concrete Test Data or Test Specs?

The input to GenSequence is a list of test vectors, in the form of a CSV file.  Each test vector specifies a single test case, but the test case may itself require a sequence or set of values (e.g., it could describe the state of a database).  In principle perhaps we could or should separate expansion of a sequence from creation of concrete data, but in practice it seems that expansion of a sequence is tied up with choice of concrete data values.  For example, one element of the input test vector might specify that a column in each row of a database is a natural number with a uniform distribution between 0 and 10 ... it does not make sense (as far as I can see) to further postpone choosing actual values. 

### Forms of output

Since we are producing concrete values, we can't put off dealing with a wide variety of forms a program under test might need.  We might be able to provide fairly generic producers of some forms of test data, but for others we will almost certainly need some kind of templating facility.   Families of output formats we will probably need include: 

* Templating for unit test frameworks (e.g., JUnit)
* Tables of values as CSV
* Templating for line-oriented input (typically for scripting languages)

And maybe ... 

* Grammar-based text file production with constraints 

The last, grammar-based text file production, is very general and might subsume the others, but it might not be the easiest to learn and use. 

