#!/bin/bash

OPTS="--colorized --color-palette darkseagreen,gold,chocolate,hotpink --only-classnames -a0"
OUTPUT="--output dot"
API_TARGET="pyzeal.rootfinders pyzeal.algorithms pyzeal.algorithms.estimators pyzeal.plugins"
FRAMEWORK_TARGET="pyzeal.utils pyzeal.pyzeal_logging pyzeal.settings pyzeal.pyzeal_types"
CLI_TARGET="pyzeal.cli"

function create_diagram {
    echo "[pyreverse]  targeting {"$1"}..."
    pyreverse $OPTS $OUTPUT $1 1>/dev/null

    echo "[dot      ]  converting results to pdf..."
    dot -Tpdf -O packages.dot classes.dot

    echo "[cleanup  ]  moving results to docs/_static..."
    rm classes.dot packages.dot
    mv classes.dot.pdf docs/_static/"$2"_classes.pdf
    mv packages.dot.pdf docs/_static/"$2"_packages.pdf
}

cd ..

echo "|---------------------------------------|"
echo "| Generating Class and Package Diagrams |"
echo "|---------------------------------------|"
echo

create_diagram "$API_TARGET" api
create_diagram "$FRAMEWORK_TARGET" framework
create_diagram "$CLI_TARGET" cli
