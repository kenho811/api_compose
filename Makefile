setup:
	python -m pip install --upgrade pip
	pip install ".[test,dist]"

unit_test:
	bash -c "cd ./tests/unit_tests/ && LOGGING__FILE_PATH='' pytest -vvvv"; \

integration_test:
	  bash -c "cd ./tests/e2e_tests/ && LOGGING__FILE_PATH='' pytest -vvvv";

check:
	python ./check_pypi_package.py

dist:
	python setup.py sdist
	twine check dist/*
	TWINE_USERNAME=$(TWINE_USERNAME) TWINE_PASSWORD=$(TWINE_PASSWORD) twine upload dist/*

clean:
	# clean all log files and reports
	find . -type f -name "*.jsonl" -delete
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.html" -not -name '*.template.html' -delete
	find . -type f -name "*.svg" -delete
	find . -type f -name "*.log" -delete
	find ./examples -type d -name "build" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +

analyse: clean
	# Generate dependency graph
	mkdir -p ./build/pydeps
	pydeps ./src/api_compose -o build/pydeps/dependency_graph.svg
