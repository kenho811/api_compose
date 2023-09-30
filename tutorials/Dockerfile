FROM jupyter/minimal-notebook:python-3.11.5

USER root

WORKDIR /home/jovyan

COPY ./setup.cfg ./setup.cfg
COPY ./setup.py ./setup.py
COPY ./README.rst ./README.rst
COPY ./src ./src

RUN pip install -e ".[tutorials]"

USER 1000


COPY ./tutorials /home/jovyan/tutorials

