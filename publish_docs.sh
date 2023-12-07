#!/bin/sh

# This script is for the author to protect docs and analysis outputs private before acceptance
# We will move docs in a privae repository tentatively during revision

for v in $(find docs/jupyternb -name "*privatedoc.ipynb")
do
    mv $v $(dirname $v)/$(basename $v "_privatedoc.ipynb").ipynb
done
