# Variables
SOURCE = ebbe

# Functions
define clean
	rm -rf *.egg-info .pytest_cache build dist
	find . -name "*.pyc" | xargs rm -f
	find . -name __pycache__ | xargs rm -rf
	rm -f *.spec
endef

# Commands
all: test
test: unit
publish: clean test upload
	$(call clean)

clean:
	$(call clean)

deps:
	pip3 install -U pip
	pip3 install -r requirements.txt

format:
	@echo Formatting code...
	black $(SOURCE) test
	@echo

unit:
	@echo Running unit tests...
	pytest -svvv
	@echo

upload:
	python setup.py sdist bdist_wheel
	twine upload dist/*
