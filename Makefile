analyse: clean
	# Generate dependency graph
	mkdir -p ./build/pydeps
	pydeps ./src/api_compose -o build/pydeps/dependency_graph.svg

build_docs:
	bash -c "cd ./docs && pip install -r requirements.txt && $(MAKE) html"

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
	python ./scripts/check_pypi_package.py $(output_file_path)

dist:
	python setup.py sdist
	twine check dist/*
	TWINE_USERNAME=$(TWINE_USERNAME) TWINE_PASSWORD=$(TWINE_PASSWORD) twine upload dist/* \

dump_model_schemas:
	python ./scripts/dump_model_schemas.py $(output_folder_path)

dump_release_version:
	python ./scripts/dump_release_version.py $(output_file_path)

integration_test:
	bash -c "cd ./src/api_compose/cli/scaffold_data && LOGGING__FILE_PATH='' pytest -vvvv";
	bash -c "cd ./tests/e2e_tests/e2e_api_server_one && LOGGING__FILE_PATH='' pytest -vvvv";

setup:
	python -m pip install --upgrade pip
	pip install ".[test,dist]"


unit_test:
	bash -c "cd ./tests/unit_tests/ && LOGGING__FILE_PATH='' pytest -vvvv"; \
