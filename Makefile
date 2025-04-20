.PHONY: setup install init-db run test test-scenario

# Install project dependencies
install:
	uv pip install -r requirements.txt

dev-install:
	uv pip install -r requirements-dev.txt

# Initialize the SQLite database
init-db:
	python src/database/schema.py

# Setup the project (install dependencies and initialize the database)
setup: install init-db

# Run the MCP server
run:
	# python3 src/dm.py
	uv run src/dm.py

# Run BDD tests using Behave
test:
	PYTHONPATH=src behave tests/features --no-capture --format pretty

# Run a specific scenario
test-scenario:
	PYTHONPATH=src behave tests/features/$(FEATURE).feature --name "$(SCENARIO)"

# If you have a venv setup section, update it
setup-venv:
	python3 -m venv venv
	. venv/bin/activate && uv pip install --upgrade pip
	. venv/bin/activate && $(MAKE) install
