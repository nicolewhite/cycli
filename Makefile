install: clean
	python setup.py install

clean:
	rm -rf build dist cycli.egg-info

test:
	py.test tests

markov:
	mkdir -p data
	python misc/markov.py
	mv markov.json cycli/