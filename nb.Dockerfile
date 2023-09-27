FROM jupyter/minimal-notebook:latest

COPY ./setup.cfg ./setup.cfg
COPY ./setup.py ./setup.py
COPY ./README.rst ./README.rst
COPY ./src ./src

RUN pip install -e .

COPY ./tutorials /home/jovyan/tutorials

