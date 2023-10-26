#!/bin/sh

sh auth.sh docker-compose.yml
docker compose up -d
sh ./lib.sh
docker start $((basename $PWD) | tr '[A-Z]' '[a-z]')-jupyterlab-1
open http://localhost:8008
