.PHONY: install install-live test lint benchmark report all

install:
	python -m pip install -e .

install-live:
	python -m pip install -e ".[live]"

test:
	pytest

lint:
	ruff check src tests

benchmark:
	python -m redcrew_arena.cli benchmark --output results

report:
	python -m redcrew_arena.cli report --results results

all: test benchmark report
