#!/bin/bash

BUILD="sphinx-build"
SRC_DIR="../docs"
BUILD_DIR="../docs/_build"
SPHINX_OPTS=""

if [ $# != 0 ]; then
    ${BUILD} -M "$1" ${SRC_DIR} ${BUILD_DIR} ${SPHINX_OPTS}
else
    echo "please choose a build target from [html | latexpdf | clean | doctest]!"
fi
