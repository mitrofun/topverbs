.PHONY: all help qa clean debug coverage coveralls

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
	DEBUG=true python3 topverbs.py -d .

# target: coverage - Test coverage
coverage:
	py.test --cov=.

# target: coveralls - Send % coverage to coveralls.io
coveralls:
	COVERALLS_REPO_TOKEN=aiHkQCR80g7rHVYDwYzuJad0tafh94uUw coveralls