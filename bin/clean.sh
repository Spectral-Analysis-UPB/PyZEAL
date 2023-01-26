#!/bin/bash

# remove logs in bin/
rm -rf logs/

# change to project root
cd ..

# remove all __pycache__ directories
rm -rf src/__pycache__
rm -rf src/*/__pycache__
rm -rf test/__pycache__
rm -rf benchmarks/__pycache__

# remove all logging directories
rm -rf logs/
rm -rf src/logs
rm -rf src/*/logs
rm -rf test/logs
rm -rf benchmarks/logs

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
rm -rf test/*/.hypothesis/

