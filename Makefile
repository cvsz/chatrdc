SHELL := /bin/sh
PYTHON ?= python3

.PHONY: help setup format lint test build security ci validate-template

help:
	@printf '%s\n' 'setup lint format test build security ci validate-template'

setup:
	$(PYTHON) -m pip install -e ".[dev]"

format:
	$(PYTHON) -m ruff format .

lint:
	$(PYTHON) -m ruff check .

test:
	$(PYTHON) -m pytest -q

build:
	$(PYTHON) -m build

security:
	pip-audit

validate-template:
	$(PYTHON) scripts/validate_repo.py
	$(PYTHON) -m unittest discover -s tests -v

ci: validate-template lint test build security
