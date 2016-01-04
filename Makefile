install: clean
	python setup.py install

clean:
	rm -rf build dist cycli.egg-info

unit:
	py.test tests

features:
	behave tests/features

test: unit features

test_all:
	neokit/neorun tests/test.sh 2.3.1 2.2.6 2.1.8

markov:
	python misc/markov.py
	echo "markov = $(<markov.txt)" > cycli/markov.py
	mv markov.txt misc

download_neo4j:
	neokit/neoget -i -x 2.3.1 2.2.6 2.1.8
	neokit/neoctl unzip 2.3.1 2.2.6 2.1.8