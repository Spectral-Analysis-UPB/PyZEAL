#!/bin/bash

cd ..
echo "starting linting, formatting and tests..."
echo ""

echo "|--------------------------------------------------|"
echo "|[running flake8 on sources, tests, and benchmarks]|"
echo "|--------------------------------------------------|"
flake8 src/ && flake8 test/ && flake8 benchmarks/ && echo "no linting errors with flake8!"
echo ""

echo "|------------------------------------------------|"
echo "|[running mypy on sources, tests, and benchmarks]|"
echo "|------------------------------------------------|"
export MYPYPATH=src && mypy src/ --namespace-packages --explicit-package-bases && mypy test/ && mypy benchmarks/ && echo "type hints look good!"
echo ""

echo "|---------------------------|"
echo "|[running pylint on sources]|"
echo "|---------------------------|"
pylint src/
echo ""

echo "|--------------------------------------------------------------|"
echo "|[running docstring coverage on sources, tests, and benchmarks]|"
echo "|--------------------------------------------------------------|"
docstr-coverage -p src/
docstr-coverage -p test/
docstr-coverage -p benchmarks/
echo ""

echo "|------------------------------------------------------------|"
echo "|[running black formatting on sources, tests, and benchmarks]|"
echo "|------------------------------------------------------------|"
black src/
black test/
black benchmarks/
echo ""

echo "|--------------------------|"
echo "|[running tests with pytest|"
echo "|--------------------------|"
pytest test/
echo ""
