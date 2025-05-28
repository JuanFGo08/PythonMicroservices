install:
	@echo "Installing dependencies..."
	python -m pip install --upgrade pip && \
		pip install -r requirements.txt
format:
	@echo "Formatting code..."
	ruff format *.py mylib/*.py database/*.py tests/*.py
lint:
	@echo "Linting code..."
	ruff check --fix *.py mylib/*.py database/*.py tests/*.py
test:
	@echo "Running tests..."
	python -m pytest -vv tests/