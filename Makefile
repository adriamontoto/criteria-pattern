full_sources = criteria_pattern tests
sources = criteria_pattern
configuration_file = pyproject.toml 


.PHONY: help
help: # Display this help
	@echo "Usage: make [COMMAND] [OPTIONS]..."
	@awk 'BEGIN {FS = ":.*#"; printf "\nCommands:\n  make \033[36m\033[0m\n"} /^[a-zA-Z_-]+:.*?#/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)


.PHONY: install
install: # Install production dependencies
	@pip install -r requirements.txt


.PHONY: install-dev
install-dev: # Install development dependencies
	@pip install -r requirements_dev.txt


.PHONY: format
format: # Automatically format python code
	@ruff check $(full_sources) --fix-only --config $(configuration_file)
	@ruff format $(full_sources) --config $(configuration_file)


.PHONY: lint
lint: # Lint python code
	@set -e; \
	mypy $(full_sources) --txt-report . --config-file $(configuration_file) || mypy_exit=$$?; \
	bandit $(sources) --recursive --configfile $(configuration_file) || bandit_exit=$$?; \
	ruff check $(full_sources) || ruff_exit=$$?; \
	exit $$(( mypy_exit || bandit_exit || ruff_exit ))


.PHONY: test
test: # Run all tests
	@pytest --config-file $(configuration_file)


.PHONY: coverage
coverage: # Get coverage report
	@set -e; \
	coverage erase; \
	coverage run -m pytest --config-file $(configuration_file) || coverage_exit=$$?; \
	coverage combine; \
	coverage report; \
	exit $$coverage_exit


.PHONY: clean
clean: # Remove all generated files
	@rm -f `find . -type f -name '*.py[co]'`
	@rm -rf `find . -name __pycache__`
	@rm -rf `find . -name .ruff_cache`
	@rm -rf `find . -name .mypy_cache`
	@rm -rf `find . -name index.txt`
	@rm -rf `find . -name .pytest_cache`
	@rm -f .coverage
	@rm -f .coverage.*
	@rm -rf coverage.xml
	@rm -rf htmlcov
