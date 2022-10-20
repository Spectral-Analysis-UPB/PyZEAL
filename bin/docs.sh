#!/bin/bash

BUILD="sphinx-build"
SRC_DIR="../docs"
BUILD_DIR="../docs/_build"
SPHINX_OPTS=""

if [ $# != 0 ]; then
    ${BUILD} -M "$1" ${SRC_DIR} ${BUILD_DIR} ${SPHINX_OPTS}
else
    echo "please choose either HTML, LATEXPDF, CLEAN or DOCTEST as build target!"
fi
