set -e
pip install -r requirements.txt


# add jupyter config
mkdir -p $HOME/.jupyter
cp jupyter_notebook_config.py $HOME/.jupyter/
cp assets/api_server_one.svg $HOME/.jupyter/
