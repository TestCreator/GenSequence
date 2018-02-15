#
#  GenSequence housekeeping
#

MODULES = makogram tests

COMPILED = __pycache__ *.pyc

ACTIVATE = source env/bin/activate

# ?? Can I use MODULES and COMPILED variables together in the
# cleanup recipe?
#
clean:
	rm -rf ${COMPILED}
	rm -rf */__pycache__   # ??
	rm -rf */*.pyc

veryclean:  clean
	rm -rf env

install:
	python3 -m venv env
	${ACTIVATE}
	pip3 install -r requirements.txt

test:
	notestests

