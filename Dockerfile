FROM python:3.12-slim-bookworm

LABEL maintainer "Thomas David, thomasdavid0@gmail.com"

WORKDIR /usr/src

COPY requirements_serve.txt /
RUN pip install --upgrade pip
RUN pip install -r /requirements_serve.txt
