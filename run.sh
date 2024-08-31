#!/usr/bin/env bash

PROJECT_NAME="champions_sim"



echo "[+] Runnning docker env:"
echo "${PROJECT_NAME}"

docker run -p 8888:8888 -v ./workdir:/home/jovyan/app $PROJECT_NAME