#!/bin/sh

# This script is for the author to protect docs and analysis outputs private before acceptance
# We will move docs in a privae repository tentatively during revision

NB_NAME = $(basename $1)
HGF_DIR = $PWD

mv $1 ~/Desktop/hgf_manuscript/hgf_docs
cd ~/Desktop/hgf_manuscript/hgf_docs
git add ~/Desktop/hgf_manuscript/hgf_docs/$NB_NAME
git commit -m ":sparkles: add $NB_NAME"
git push origin main

cd $HGF_DIR
cp $(basename $PWD)/docs/jupyternb/README.ipynb $(basename $PWD)/docs/jupyternb/$NB_NAME
