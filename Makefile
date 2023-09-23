analyse: clean
	# Generate dependency graph
	mkdir -p ./build/pydeps
	pydeps ./src/api_compose -o build/pydeps/dependency_graph.svg

clean:
	# clean all log files and reports
	find . -type f -name "*.jsonl" -delete
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.html" -not -name '*.template.html' -delete
	find . -type f -name "*.svg" -delete
	find . -type f -name "*.log" -delete
	find ./examples -type d -name "build" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +

check:
	python ./check_pypi_package.py 'result.txt'

dist:
	python setup.py sdist
	twine check dist/*
	TWINE_USERNAME=$(TWINE_USERNAME) TWINE_PASSWORD=$(TWINE_PASSWORD) twine upload dist/* \

build_docs:
	cp -r ./tutorials/lesson_* ./docs/source/docs/tutorials
	bash -c "cd ./docs && pip install -r requirements.txt && $(MAKE) html"

integration_test:
	 bash -c "cd ./tests/e2e_tests/e2e_scaffold && LOGGING__FILE_PATH='' pytest -vvvv";

setup:
	python -m pip install --upgrade pip
	pip install ".[test,dist]"


unit_test:
	bash -c "cd ./tests/unit_tests/ && LOGGING__FILE_PATH='' pytest -vvvv"; \
