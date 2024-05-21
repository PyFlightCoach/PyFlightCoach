FROM python:3.12-slim-bookworm

LABEL maintainer "Thomas David, thomasdavid0@gmail.com"

WORKDIR /usr/src

COPY requirements.txt /
RUN pip install --upgrade pip
RUN pip install -r /requirements.txt
RUN pip install ardupilot-log-reader
RUN pip install pfc-geometry
RUN pip install flightdata
RUN pip install flightanalysis
RUN pip install flightplotting
RUN pip install droneinterface
