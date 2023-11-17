#!/bin/sh

sh auth.sh docker-compose.yml
docker compose up -d
docker start $((basename $PWD) | tr '[A-Z]' '[a-z]')-jupyterlab-1
docker exec $((basename $PWD) | tr '[A-Z]' '[a-z]')-jupyterlab-1 sudo pip -U pip
sh ./lib.sh
docker exec $((basename $PWD) | tr '[A-Z]' '[a-z]')-jupyterlab-1 sudo pip -U pip
docker exec $((basename $PWD) | tr '[A-Z]' '[a-z]')-jupyterlab-1 Rscript ./tools/bioinfo_installer.R
sh ./writelib.sh
open http://localhost:8008
