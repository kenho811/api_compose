#!/bin/bash

set -e

pip install -r ./requirements.txt
cd ./api_server_one

./app.py # start the HTTP server
echo 'please check http://localhost:8080/ui'
