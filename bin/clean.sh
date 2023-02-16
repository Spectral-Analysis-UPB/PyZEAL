#!/bin/bash

# remove logs in bin/
rm -rf logs/

# change to project root
cd ..

# remove pytest related stuff in project root
rm -rf .mypy_cache
rm -rf .pytest_cache
if [[ -f ".coverage" ]]; then rm .coverage; fi
rm -rf htmlcov

# remove all __pycache__ directories
rm -rf src/__pycache__
rm -rf src/*/__pycache__
rm -rf src/*/*/__pycache__
rm -rf tests/__pycache__
rm -rf tests/*/__pycache__
rm -rf tests/*/*/__pycache__

# remove all logging directories
rm -rf logs/
rm -rf src/logs
rm -rf src/*/logs
rm -rf src/*/*/logs
rm -rf tests/logs
rm -rf tests/*/logs

# remove documentation build artifacts
rm -rf docs/_build/html/
rm -rf docs/_build/doctrees/
rm -rf docs/_build/pdf/

# remove python build artifacts
rm -rf dist/
rm -rf ./build/
rm -rf src/*.egg-info/
rm -rf .hypothesis/
rm -rf src/*/.hypothesis/
rm -rf tests/.hypothesis/
rm -rf tests/*/.hypothesis/
