#!/bin/sh

# This script is for the author to protect docs and analysis outputs private before acceptance
# We will move docs in a privae repository tentatively during revision

NB_NAME = $(basename $1)

mv $1 ~/Desktop/hgf_manuscript/hgf_docs
cp $(basename $PWD)/docs/jupyternb/README.ipynb $1
git add $1
git commit -m ":construction::books: add tentative doc ($(basename $1))"
cd ~/Desktop/hgf_manuscript/hgf_docs
git add ~/Desktop/hgf_manuscript/hgf_docs/$(basename $1)
git commit -m ":sparkles: add $(basename $1)"
git push origin main
