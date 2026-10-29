SHELL := /bin/sh
PYTHON ?= python3
APP_PYTHON := agent mcp_server tests

.PHONY: help setup format lint test build security ci validate-template

help:
	@printf '%s\n' 'setup lint format test build security ci validate-template'

setup:
	$(PYTHON) -m pip install -e ".[dev]"

format:
	$(PYTHON) -m ruff format $(APP_PYTHON)

lint:
	$(PYTHON) -m ruff check $(APP_PYTHON)

test:
	$(PYTHON) -m pytest -q

build:
	$(PYTHON) -m build

security:
	pip-audit

validate-template:
	$(PYTHON) scripts/validate_repo.py
	$(PYTHON) -m unittest discover -s tests -p 'test_bootstrap.py' -v

ci: validate-template lint test build security
