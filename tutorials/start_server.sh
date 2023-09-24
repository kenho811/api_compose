#!/bin/bash

set -e

pip install -r ./requirements.txt
cd ./api_server_one

pipenv install --dev && pipenv shell
./app.py # start the HTTP server

echo 'please check http://localhost:8080/ui'
