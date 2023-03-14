#!/bin/bash

cd ..
echo "starting formatting, linting, type checking [and tests]..."
echo "--- use '--tests' to also run tests ---"
echo ""

echo "|-----------------------------------------------------------|"
echo "|[running black and isort on sources, tests, and benchmarks]|"
echo "|-----------------------------------------------------------|"
black pyzeal/
black tests/
isort pyzeal/
isort tests/
echo ""

echo "|--------------------------------------------------|"
echo "|[running flake8 on sources, tests, and benchmarks]|"
echo "|--------------------------------------------------|"
flake8 pyzeal/ tests/ \
    && echo "no linting errors with flake8!"
echo ""

echo "|-------------------------------------|"
echo "|[running pylint on tests and sources]|"
echo "|-------------------------------------|"
pylint pyzeal/ tests/
echo ""

echo "|------------------------------------------------|"
echo "|[running mypy on sources, tests, and benchmarks]|"
echo "|------------------------------------------------|"
mypy --explicit-package-bases pyzeal/ \
    && mypy tests/ \
    && echo "type hints look good!"
echo ""

echo "|--------------------------------------------------------------|"
echo "|[running docstring coverage on sources, tests, and benchmarks]|"
echo "|--------------------------------------------------------------|"
docstr-coverage -b docs/_static/ -p pyzeal/ tests/
echo ""

echo "|--------------------------|"
echo "|[validating json schemata]|"
echo "|--------------------------|"
check-jsonschema -v --schemafile pyzeal/settings/settings_schema.json \
    pyzeal/settings/default_settings.json
if [[ -e pyzeal/settings/custom_settings.json ]]
then
    check-jsonschema -v --schemafile pyzeal/settings/settings_schema.json \
        pyzeal/settings/custom_settings.json
fi
echo ""

if [[ "$1" == "--tests" ]]
then
    echo "|---------------------------|"
    echo "|[running tests with pytest]|"
    echo "|---------------------------|"
    pytest --cov=pyzeal/ --cov-report=html tests/
    echo ""
fi

echo "|-------------------------|"
echo "|[testing CLI entry point]|"
echo "|-------------------------|"
pyzeal --version
echo ""

echo "--> all done!"
