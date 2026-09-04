SHELL := /usr/bin/env bash
.SHELLFLAGS := -eu -o pipefail -c

SOURCES = criteria_pattern
FULL_SOURCES = $(SOURCES) tests
CONFIGURATION_FILE = pyproject.toml 
CI ?= false
VERBOSE ?= false
PYTHON_VERSION ?= 3.14
PYTHON_VERSIONS ?= 3.11,3.12,3.13,3.14
PYTHON_VIRTUAL_ENVIRONMENT ?= .venv$(PYTHON_VERSION)
UV_BIN ?= uv
GROUP ?= all
COVERAGE_DATA_FILES ?= coverage/.coverage_*
COVERAGE_HTML_TITLE ?= Coverage report
COVERAGE_CONTEXT ?= $(if $(CONTEXT),$(CONTEXT),python-$(PYTHON_VERSION))

COMMA := ,
EMPTY :=
SPACE := $(EMPTY) $(EMPTY)
PYTHON_VERSION_LIST := $(subst $(COMMA),$(SPACE),$(PYTHON_VERSIONS))

ifeq ($(CI), true)
    PYTHON_BIN = python
else
    PYTHON_BIN = $(PYTHON_VIRTUAL_ENVIRONMENT)/bin/python$(PYTHON_VERSION)
endif


define quiet
	@if [ "$(VERBOSE)" = "true" ]; then \
		$(1); \
	else \
		$(1) > /dev/null; \
	fi
endef


.PHONY: help
help: # It displays this help message
	@printf "\nUsage: make [COMMAND] [OPTIONS]...\n"
	@awk 'BEGIN {FS = ":.*#"; printf "\nCommands:\n  make \033[36m\033[0m\n"} /^[a-zA-Z_-]+:.*?#/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)
	@printf "\nOptions (override with VAR=value):\n"
	@printf "  %-40s %s\n" "VERBOSE=$(VERBOSE)"                   "Show command output (true/false)"
	@printf "  %-40s %s\n" "CI=$(CI)"                       	  "Indicates if the script is running in a CI environment (true/false)"
	@printf "  %-40s %s\n" "PYTHON_VERSION=$(PYTHON_VERSION)"     "Used python interpreter for creating the virtual environment"
	@printf "  %-40s %s\n" "PYTHON_VERSIONS=$(PYTHON_VERSIONS)"   "Used python interpreters for all-version targets"
	@printf "  %-40s %s\n" "PYTHON_VIRTUAL_ENVIRONMENT=$(PYTHON_VIRTUAL_ENVIRONMENT)" "Name of the virtual environment folder"
	@printf "  %-40s %s\n" "GROUP=$(GROUP)"                       "Group of dependencies to install (all, coverage, format, lint, release, test, types)"
	@printf "  %-40s %s\n" "COVERAGE_DATA_FILES=$(COVERAGE_DATA_FILES)" "Coverage data files to combine"
	@printf "  %-40s %s\n" "COVERAGE_HTML_TITLE=$(COVERAGE_HTML_TITLE)" "Title for the generated coverage HTML report"
	@printf "  %-40s %s\n" "COVERAGE_CONTEXT=$(COVERAGE_CONTEXT)" "Context label for coverage runs"
	@printf "\n"


.PHONY: setup
setup: # It setups the project, creates the virtual environment and installs the dependencies
	@$(MAKE) --no-print-directory setup-python
	@$(MAKE) --no-print-directory setup-hooks


.PHONY: setup-python
setup-python:
	@echo -e "\n⌛ Setting up the project...\n"

	$(call quiet, $(UV_BIN) venv $(PYTHON_VIRTUAL_ENVIRONMENT) --python $(PYTHON_VERSION) --clear)
	$(call quiet, $(MAKE) --no-print-directory install GROUP=$(GROUP))
	$(call quiet, $(MAKE) --no-print-directory install GROUP=develop)

	@echo -e "\n✅ Run 'source $(PYTHON_VIRTUAL_ENVIRONMENT)/bin/activate' to activate the virtual environment.\n"


.PHONY: setup-hooks
setup-hooks:
	$(call quiet, $(PYTHON_BIN) -m pre_commit install --hook-type pre-commit --hook-type commit-msg)


.PHONY: setup-all
setup-all: # It setups all configured Python versions
	@echo -e "\n⌛ Setting up all configured Python versions...\n"

	@set -e; \
	for python_version in $(PYTHON_VERSION_LIST); do \
		$(MAKE) --no-print-directory setup-python \
			PYTHON_VERSION=$$python_version \
			PYTHON_VIRTUAL_ENVIRONMENT=.venv$$python_version \
			GROUP=$(GROUP); \
	done

	$(call quiet, $(MAKE) --no-print-directory setup-hooks)

	@echo -e "\n✅ All configured Python versions set up correctly. Run 'source .venv<PYTHON_VERSION>/bin/activate' to activate the virtual environment for a specific Python version.\n"


.PHONY: install
install: # Installs the project dependencies, use the GROUP variable to install only a specific group of dependencies
	@echo -e "\n⌛ Installing dependencies...\n"

ifeq ($(GROUP), production)
ifeq ($(CI), true)
	$(call quiet, $(UV_BIN) export --frozen --no-emit-project --no-default-groups | $(UV_BIN) pip install --system --python $(PYTHON_BIN) --requirements -)
else
	$(call quiet, UV_PROJECT_ENVIRONMENT="$(PYTHON_VIRTUAL_ENVIRONMENT)" $(UV_BIN) sync --frozen --inexact --no-active --no-install-project --no-default-groups --python $(PYTHON_VERSION))
endif
else
ifeq ($(CI), true)
	$(call quiet, $(UV_BIN) export --frozen --no-emit-project --no-default-groups $(if $(filter all,$(GROUP)),--all-groups,--group $(GROUP)) | $(UV_BIN) pip install --system --python $(PYTHON_BIN) --requirements -)
else
	$(call quiet, UV_PROJECT_ENVIRONMENT="$(PYTHON_VIRTUAL_ENVIRONMENT)" $(UV_BIN) sync --frozen --inexact --no-active --no-install-project --no-default-groups $(if $(filter all,$(GROUP)),--all-groups,--group $(GROUP)) --python $(PYTHON_VERSION))
endif
endif


	@echo -e "\n✅ Dependencies installed correctly.\n"


.PHONY: format
format: # It automatically formats code
	@echo -e "\n⌛ Formatting project code...\n"

	@$(PYTHON_BIN) -m ruff check $(FULL_SOURCES) --config $(CONFIGURATION_FILE) --fix-only
	@$(PYTHON_BIN) -m ruff format $(FULL_SOURCES) --config $(CONFIGURATION_FILE)

	@echo -e "\n✅ Code formatted correctly.\n"


.PHONY: lint
lint: # It automatically lints code
	@echo -e "\n⌛ Linting project code...\n"

	@set -e; \
	ty_exit=0; \
	ruff_exit=0; \
	$(PYTHON_BIN) -m ty check $(FULL_SOURCES) --python $(PYTHON_BIN) || ty_exit=$$?; \
	$(PYTHON_BIN) -m ruff check $(FULL_SOURCES) --config $(CONFIGURATION_FILE) --no-fix || ruff_exit=$$?; \
	exit $$(( ty_exit || ruff_exit ))

	@echo -e "\n✅ Code linted correctly.\n"


.PHONY: test
test: # It runs all tests
	@echo -e "\n⌛ Running tests...\n"

	@$(PYTHON_BIN) -m pytest --config-file $(CONFIGURATION_FILE)

	@echo -e "\n✅ Tests run correctly.\n"


.PHONY: test-all
test-all: # It runs all tests for all configured Python versions
	@set -e; \
	for python_version in $(PYTHON_VERSION_LIST); do \
		$(MAKE) --no-print-directory test \
			PYTHON_VERSION=$$python_version \
			PYTHON_VIRTUAL_ENVIRONMENT=.venv$$python_version; \
	done


.PHONY: coverage
coverage: # It gets the test coverage report
	@echo -e "\n⌛ Getting test coverage report...\n"

	$(call quiet, rm -rf coverage .coverage .coverage.*)
	$(call quiet, mkdir -p coverage)

	@set -e; \
	coverage_exit=0; \
	COVERAGE_FILE=$${COVERAGE_FILE:-coverage/.coverage_python_$(PYTHON_VERSION)} \
		$(MAKE) --no-print-directory coverage-run || coverage_exit=$$?; \
	$(MAKE) --no-print-directory coverage-report; \
	exit $$coverage_exit

	@echo -e "\n✅ Test coverage report generated correctly.\n"


.PHONY: coverage-run
coverage-run:
	@echo -e "\n⌛ Running tests with coverage...\n"

	@$(PYTHON_BIN) -m coverage run --context="$(COVERAGE_CONTEXT)" --module pytest --config-file $(CONFIGURATION_FILE)


.PHONY: coverage-report
coverage-report: # It combines coverage data and generates terminal and HTML reports
	@echo -e "\n⌛ Generating coverage report...\n"

	@set -e; \
	$(PYTHON_BIN) -m coverage combine $(COVERAGE_DATA_FILES); \
	$(PYTHON_BIN) -m coverage report; \
	$(PYTHON_BIN) -m coverage html --show-contexts --title "$(COVERAGE_HTML_TITLE)"

	@echo -e "\n✅ Coverage report generated correctly.\n"


.PHONY: coverage-all
coverage-all: # It gets the test coverage report for all configured Python versions
	@echo -e "\n⌛ Getting test coverage report for all configured Python versions...\n"

	$(call quiet, rm -rf coverage .coverage .coverage.*)
	$(call quiet, mkdir -p coverage)

	@set -e; \
	coverage_exit=0; \
	for python_version in $(PYTHON_VERSION_LIST); do \
		COVERAGE_FILE=coverage/.coverage_python_$$python_version \
			$(MAKE) --no-print-directory coverage-run \
				PYTHON_VERSION=$$python_version \
				PYTHON_VIRTUAL_ENVIRONMENT=.venv$$python_version || coverage_exit=$$?; \
	done; \
	$(MAKE) --no-print-directory coverage-report; \
	exit $$coverage_exit

	@echo -e "\n✅ Test coverage report generated correctly.\n"


.PHONY: build-code
build-code: # It builds the project
	@echo -e "\n⌛ Building project...\n"

	$(call quiet, $(PYTHON_BIN) -m build)

	@echo -e "\n✅ Project built correctly.\n"


.PHONY: audit
audit: # It audits dependencies and source code
	@echo -e "\n⌛ Running security audit...\n"

	@$(UV_BIN) audit

	@echo -e "\n✅ Security audit completed correctly.\n"


.PHONY: secrets
secrets: # It checks for secrets in the source code
	@echo -e "\n⌛ Checking secrets...\n"

	@$(PYTHON_BIN) -m pre_commit run gitleaks --all-files

	@echo -e "\n✅ Secrets checked correctly.\n"


.PHONY: clean
clean: # It cleans up the project, removing the virtual environment and some files
	@echo -e "\n⌛ Cleaning up the project...\n"

	$(call quiet, if [ -x "$(PYTHON_BIN)" ]; then $(PYTHON_BIN) -m pre_commit clean || true; fi)
	$(call quiet, if [ -x "$(PYTHON_BIN)" ]; then $(PYTHON_BIN) -m pre_commit uninstall --hook-type pre-commit --hook-type commit-msg || true; fi)
	$(call quiet, for python_version in $(PYTHON_VERSION_LIST); do rm -rf .venv$$python_version; done)
	$(call quiet, rm -rf `find . -type f -name '*.py[co]'`)
	$(call quiet, rm -rf `find . -name __pycache__`)
	$(call quiet, rm -rf `find . -name .ruff_cache`)
	$(call quiet, rm -rf `find . -name .mypy_cache`)
	$(call quiet, rm -rf `find . -name .pytest_cache`)
	$(call quiet, rm -rf .coverage)
	$(call quiet, rm -rf .coverage.*)
	$(call quiet, rm -rf coverage)
	$(call quiet, rm -rf coverage.xml)
	$(call quiet, rm -rf htmlcov)

	@echo -e "\n✅ Run 'deactivate' to deactivate the virtual environment.\n"
