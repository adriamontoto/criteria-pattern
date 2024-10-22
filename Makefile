FULL_SOURCES = criteria_pattern
SOURCES = criteria_pattern
CONFIGURATION_FILE = pyproject.toml 


.PHONY: help
help: # Display this help
	@echo "Usage: make [COMMAND] [OPTIONS]..."
	@awk 'BEGIN {FS = ":.*#"; printf "\nCommands:\n  make \033[36m\033[0m\n"} /^[a-zA-Z_-]+:.*?#/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)


.PHONY: install
install: # Install dependencies
	@make install-dev


.PHONY: install-dev
install-dev: # Install development dependencies
	@pip install --requirement requirements_dev.txt


.PHONY: install-prod
install-prod: # Install production dependencies
	@pip install --requirement requirements.txt


.PHONY: format
format: # Automatically format python code
	@ruff check $(FULL_SOURCES) --fix-only --config $(CONFIGURATION_FILE)
	@ruff format $(FULL_SOURCES) --config $(CONFIGURATION_FILE)


.PHONY: lint
lint: # Lint python code
	@set -e; \
	mypy $(FULL_SOURCES) --txt-report . --config-file $(CONFIGURATION_FILE) || mypy_exit=$$?; \
	bandit $(SOURCES) --recursive --configfile $(CONFIGURATION_FILE) || bandit_exit=$$?; \
	ruff check $(FULL_SOURCES) || ruff_exit=$$?; \
	exit $$(( mypy_exit || bandit_exit || ruff_exit ))


.PHONY: test
test: # Run all tests
	@pytest --config-file $(CONFIGURATION_FILE)


.PHONY: coverage
coverage: # Get coverage report
	@set -e; \
	coverage erase; \
	coverage run --module pytest --config-file $(CONFIGURATION_FILE) || coverage_exit=$$?; \
	coverage combine; \
	coverage report; \
	exit $$coverage_exit


.PHONY: clean
clean: # Remove all generated files
	@rm --force --recursive `find . -type f -name '*.py[co]'`
	@rm --force --recursive `find . -name __pycache__`
	@rm --force --recursive `find . -name .ruff_cache`
	@rm --force --recursive `find . -name .mypy_cache`
	@rm --force --recursive `find . -name index.txt`
	@rm --force --recursive `find . -name .pytest_cache`
	@rm --force --recursive .coverage
	@rm --force --recursive .coverage.*
	@rm --force --recursive coverage.xml
	@rm --force --recursive htmlcov
