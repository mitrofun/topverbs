.PHONY: all help qa clean debug coverage coveralls build setup-test

# target: all - Default target. Does nothing.
all:
	@clear
	@echo "Hello $(LOGNAME), nothing to do by default"
	@echo "Try 'make help'"

# target: help - Display callable targets.
help:
	@clear
	@egrep "^# target:" [Mm]akefile

# target: qa - Run tests
qa:
	pytest

# target: clean - Delete pycache
clean:
	echo "### Cleaning *.pyc and .DS_Store files "
	find . -name '*.pyc' -exec rm -f {} \;
	find . -name '.DS_Store' -exec rm -f {} \;
	find . -name "__pycache__" -type d -exec rm -rf {} +

# target: debug - Run script in debug mode
debug:
	DEBUG=true python3 topverbs/topverbs.py -d .

# target: coverage - Test coverage
coverage:
	py.test --cov=.

# target: coveralls - Update info in coveralls.io (dev)
coveralls:
	coverage run --source=./topverbs setup.py test && COVERALLS_REPO_TOKEN=hO9WNNcZxAgWn9YPrLNrDoef0MrI9lU2x coveralls

# target: build - Build pkg
build:
	python setup.py sdist

# target: setup-test - Test setup py
setup-test:
	python setup.py test

# target: docker-build - Build docker image with tag habrpars
docker-build:
	docker build . -t topverbs

# target: docker-test - Test code in docker
docker-test:
	docker run --rm topverbs python3 setup.py test