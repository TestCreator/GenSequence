#
#  GenSequence housekeeping
#

MODULES = makogram tests

COMPILED = __pycache__ *.pyc

ACTIVATE = source "./env/bin/activate"

# ?? Can I use MODULES and COMPILED variables together in the
# cleanup recipe?
#

ready: earthquakes
	mv parsey/junk/outgoing.py .
	#python3 outgoing.py
	python3 earthquakegen.py
	python3 demos/eqanalysis/eqanalysis.py ~/Documents/GenSequence/cases1/11-70-Mags\:right_slanted-Lats\:_cardioid-Longs\:left_slanted-Depths\:uniform-.csv plot magnitudes

earthquakes:
	${ACTIVATE}
	cd ~/Documents/GenSequence
	python3 ~/Documents/GenPairs/genpairs.py < earthquakegen.cp -c -o > earthquakegentestvectors.csv
	echo "    Generated pair-wise symbolic test vectors!"
	python3 parsey/write_prm.py -s "simple_earthquaker.prm" -t "parsey/prm-blueprints/masterTemplate" -d "parsey/junk/outgoing.py"
	echo "Wrote half of the gen file! Now go to outgoing.py and write in your grammar! When you are done, run make ready"

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

