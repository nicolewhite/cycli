install: clean
	python setup.py install

clean:
	rm -rf build dist cycli.egg-info

test:
	py.test tests

markov:
	python misc/markov.py
	echo "markov = $(<markov.txt)" > cycli/markov.py
	mv markov.txt misc