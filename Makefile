.PHONY: check test

PYTHON ?= python3

# Stdlib only: every file compiles, and no ambiguous indentation.
check:
	$(PYTHON) -m compileall -q ledgerlite tests
	$(PYTHON) -m tabnanny ledgerlite tests

test:
	$(PYTHON) -m unittest discover -s tests -t . -v
