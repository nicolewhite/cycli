install: clean
	python setup.py install

clean:
	rm -rf build dist cycli.egg-info

test:
	python -m unittest

markov:
	mkdir -p data
	python misc/markov.py
	mv markov.json cycli/