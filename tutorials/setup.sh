set -e
pip install -r requirements.txt


# add jupyter config
mkdir -p /tmp/.jupyter
cp assets/api_server_one.svg /tmp/.jupyter/
