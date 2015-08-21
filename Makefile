install: clean
	python setup.py install

clean:
	rm -rf build dist cycli.egg-info

test:
	python -m unittest