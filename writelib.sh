#!/bin/sh

docker exec -it $((basename $PWD) | tr '[A-Z]' '[a-z]')-jupyterlab-1 sudo pip list --format=freeze > ./tools/requirements_py.txt
docker exec $((basename $PWD) | tr '[A-Z]' '[a-z]')-jupyterlab-1 Rscript ./tools/export_deps.R
