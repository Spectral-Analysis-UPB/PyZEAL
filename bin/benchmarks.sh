#!/bin/bash

cd ../

if [[ "$1" != "--benchmark" && "$1" != "--preview" ]]
then
    echo "usage: --preview   (start browser preview for existing benchmarks)"
    echo "       --benchmark (benchmark the most recent commit)"
fi

if [[ "$1" == "--benchmark" || "$2" == "--benchmark" ]]
then
    echo "[asv] running benchmarks for pyzeal..."
    asv run
    asv publish
fi

if [[ "$1" == "--existing" || "$2" == "--existing" ]]
then
    echo "[asv] running benchmarks for commits with pre-existing benchmarks..."
    asv run EXISTING
    asv publish
fi

if [[ "$1" == "--preview" || "$2" == "--preview" ]]
then
    echo "[asv] starting browser preview of benchmarks..." 
    asv preview
fi
