#!/bin/sh

docker exec $((basename $PWD) | tr '[A-Z]' '[a-z]')-jupyterlab-1 python -m pip install -r ./tools/requirements_py.txt
docker exec $((basename $PWD) | tr '[A-Z]' '[a-z]')-jupyterlab-1 Rscript ./tools/install_deps.R
