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
	python neokit/neorun.py tests/test.sh 2.3.3 2.2.9 2.1.8

markov:
	python misc/markov.py
	echo "markov = $(<markov.txt)" > cycli/markov.py
	mv markov.txt misc

download_neo4j:
	python neokit/neoget.py -i -x 2.3.3 2.2.9 2.1.8
	python neokit/neoctl.py unzip 2.3.3 2.2.9 2.1.8

register:
	python setup.py register -r pypi

upload:
	python setup.py sdist upload -r pypi
