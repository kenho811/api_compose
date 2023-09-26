FROM python:3.11.5-slim-bullseye

WORKDIR /usr/src/app

COPY ./setup.cfg ./setup.cfg
COPY ./setup.py ./setup.py
COPY ./README.rst ./README.rst


RUN ls
RUN pip install .
ENTRYPOINT ["acp"]