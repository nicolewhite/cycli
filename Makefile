install: clean
	python setup.py install

clean:
	rm -rf build dist cycli.egg-info

unit:
	py.test tests

features:
	behave tests/features

test: unit features

markov:
	python misc/markov.py
	echo "markov = $(<markov.txt)" > cycli/markov.py
	mv markov.txt misc