run := poetry run

.PHONY: test
test:
	$(run) pytest tests/ $(ARGS)

.PHONY: test-coverage
test-coverage:
	$(run) pytest tests/ --cov-report term-missing --cov=kassalappy $(ARGS)

.PHONY: coverage
coverage:
	$(run) coverage html

.PHONY: format
format:
	$(run) ruff format kassalappy

.PHONY: format-check
format-check:
	$(run) ruff --check kassalappy

.PHONY: setup
setup:
	poetry install

.PHONY: update
update:
	poetry update

.PHONY: repl
repl:
	$(run) python

