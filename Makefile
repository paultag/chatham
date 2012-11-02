# Copyright (c) Paul Tagliamonte <paultag@debian.org> under the terms
# of chatham it's self.

all: build

lint: clean
	@flake8 . -r

develop: build
	@python setup.py develop

install: build
	@python setup.py install

build:
	@python setup.py build

clean:
	@python setup.py clean
	@rm -rvf chatham.egg-info
	@rm -rvf build
