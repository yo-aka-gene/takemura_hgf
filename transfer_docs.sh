#!/bin/sh

# This script is for the author to protect docs and analysis outputs private before acceptance
# We will move docs in a privae repository tentatively during revision

NB_NAME = $(basename $1)

mv $1 ~/Desktop/hgf_manuscript/hgf_docs
cp $(basename $PWD)/docs/jupyternb/README.ipynb $(basename $PWD)/docs/jupyternb/$NB_NAME
git add $(basename $PWD)/docs/jupyternb/$NB_NAME
git commit -m ":construction::books: add tentative doc ($NB_NAME)"
cd ~/Desktop/hgf_manuscript/hgf_docs
git add ~/Desktop/hgf_manuscript/hgf_docs/$NB_NAME
git commit -m ":sparkles: add $NB_NAME"
git push origin main
