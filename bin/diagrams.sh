#!/bin/bash

cd ..

echo "|---------------------------------------|"
echo "| Generating Class and Package Diagrams |"
echo "|---------------------------------------|"
echo

OPTS="--colorized --color-palette darkseagreen,gold,chocolate,hotpink --only-classnames -a0"
OUTPUT="--output dot"
TARGET="pyzeal.rootfinders pyzeal.algorithms pyzeal.pyzeal_logging pyzeal.utils"

echo "[pyreverse]  targeting {"$TARGET"}..."
pyreverse $OPTS $OUTPUT $TARGET 1>/dev/null

echo "[dot      ]  converting results to pdf..."
dot -Tpdf -O packages.dot classes.dot

echo "[cleanup  ]  moving results to docs/_static..."
rm classes.dot packages.dot
mv classes.dot.pdf docs/_static/class_diagram1.pdf
mv packages.dot.pdf docs/_static/package_diagram1.pdf
