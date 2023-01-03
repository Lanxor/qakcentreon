
all: install-dep

install-dep:
	python3 -m pip install -r requirements.txt

check: lint unittest testcoverage

lint:
	flake8 qakcentreon

unittest:
	python3 -m unittest discover -s tests

testcoverage:
	python3 -m coverage run --source qakcentreon -m unittest discover -s tests
	python3 -m coverage report -m
  
