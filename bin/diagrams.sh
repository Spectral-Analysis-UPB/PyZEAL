#!/bin/bash

cd ..

echo "|---------------------------------------|"
echo "| Generating Class and Package Diagrams |"
echo "|---------------------------------------|"
echo

OPTS="--colorized --color-palette darkseagreen,gold,chocolate,hotpink --only-classnames -a0"
OUTPUT="--output dot"
API_TARGET="pyzeal.rootfinders pyzeal.algorithms pyzeal.algorithms.estimators pyzeal.plugins"
FRAMEWORK_TARGET="pyzeal.utils pyzeal.pyzeal_logging pyzeal.settings pyzeal.pyzeal_types"
CLI_TARGET="pyzeal.cli"

echo "[pyreverse]  targeting {"$API_TARGET"}..."
pyreverse $OPTS $OUTPUT $API_TARGET 1>/dev/null

echo "[dot      ]  converting results to pdf..."
dot -Tpdf -O packages.dot classes.dot

echo "[cleanup  ]  moving results to docs/_static..."
rm classes.dot packages.dot
mv classes.dot.pdf docs/_static/api_classes.pdf
mv packages.dot.pdf docs/_static/api_packages.pdf

echo "[pyreverse]  targeting {"$FRAMEWORK_TARGET"}..."
pyreverse $OPTS $OUTPUT $FRAMEWORK_TARGET 1>/dev/null

echo "[dot      ]  converting results to pdf..."
dot -Tpdf -O packages.dot classes.dot

echo "[cleanup  ]  moving results to docs/_static..."
rm classes.dot packages.dot
mv classes.dot.pdf docs/_static/framework_classes.pdf
mv packages.dot.pdf docs/_static/framework_packages.pdf

echo "[pyreverse]  targeting {"$CLI_TARGET"}..."
pyreverse $OPTS $OUTPUT $CLI_TARGET 1>/dev/null

echo "[dot      ]  converting results to pdf..."
dot -Tpdf -O packages.dot classes.dot

echo "[cleanup  ]  moving results to docs/_static..."
rm classes.dot packages.dot
mv classes.dot.pdf docs/_static/cli_classes.pdf
mv packages.dot.pdf docs/_static/cli_packages.pdf
