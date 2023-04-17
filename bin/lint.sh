#!/bin/bash

cd ..
echo "starting formatting, linting, type checking [and tests]..."
echo "--- use '--tests' to also run tests ---"
echo ""

echo "|-----------------------------------------------------------|"
echo "|[running black and isort on sources, tests, and benchmarks]|"
echo "|-----------------------------------------------------------|"
black pyzeal/
isort pyzeal/
echo ""

echo "|---------------------------------------------------|"
echo "|[running linters on sources, tests, and benchmarks]|"
echo "|---------------------------------------------------|"
pylama pyzeal/ && echo "no linting errors with pylama!"
pylint pyzeal/
echo ""

echo "|------------------------------------------------|"
echo "|[running mypy on sources, tests, and benchmarks]|"
echo "|------------------------------------------------|"
mypy pyzeal/ && echo "type hints look good!"
echo ""

echo "|--------------------------------------------------------------|"
echo "|[running docstring coverage on sources, tests, and benchmarks]|"
echo "|--------------------------------------------------------------|"
docstr-coverage -b docs/_static/ -p pyzeal/
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

    PARALLEL=""
    shift

    while [[ "$#" -ge 1 ]]
    do
        if [[ "$1" == "--parallel" ]]
        then
            PARALLEL="-n auto"
        fi
        shift
    done

    pytest --cov=pyzeal/ --cov-report=html  $PARALLEL pyzeal/tests/
    pytest --cov=pyzeal/ --cov-report=html --cov-append -m "locator" pyzeal/tests/
    echo ""
fi

echo "|-------------------------|"
echo "|[testing CLI entry point]|"
echo "|-------------------------|"
pyzeal --version
echo ""

echo "--> all done!"
