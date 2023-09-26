FROM jupyter/minimal-notebook:latest
COPY requirements.txt /home/jovyan
RUN pip install -r /home/jovyan/requirements.txt

COPY . /home/jovyan

