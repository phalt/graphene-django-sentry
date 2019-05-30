FROM python:3.6-alpine

RUN apk update
RUN apk upgrade
RUN apk add --update python python-dev py-pip build-base

RUN adduser -Ds /bin/bash python

WORKDIR /home/python

ADD . /home/python
ADD requirements_dev.txt /home/python/requirements_dev.txt

RUN pip install --upgrade pip
RUN pip install -r requirements_dev.txt

USER python
