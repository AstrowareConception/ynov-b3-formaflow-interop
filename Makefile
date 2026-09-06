PYTHON ?= python

.PHONY: setup start stop reset-data contracts generate benchmark test test-unit test-contracts test-compatibility test-integration smoke lint typecheck quality validate-repo validate-diagrams validate-handoff package
setup start stop reset-data contracts generate benchmark test test-unit test-contracts test-compatibility test-integration smoke lint typecheck quality validate-repo validate-diagrams validate-handoff package:
	$(PYTHON) scripts/tasks.py $@

