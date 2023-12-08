#!/bin/sh

# This script is for the author to protect docs and analysis outputs private before acceptance
# We will move docs in a privae repository tentatively during revision

 mv $1 $(dirname $1)/$(basename $1 "_privatedoc.ipynb").ipynb
