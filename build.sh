#!/usr/bin/env bash

PROJECT_NAME="champions_sim"


echo "[+] Build docker image:"
echo "${PROJECT_NAME}"

docker build -t $PROJECT_NAME  .