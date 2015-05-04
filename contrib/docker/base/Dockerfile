FROM ubuntu:14.04
MAINTAINER PyLabs pylabs@allegrogroup.com

RUN apt-get update && apt-get install -y \
    python \
    python-dev \
    python-virtualenv \
    redis-server \
    supervisor

RUN virtualenv /opt/tipboard

VOLUME /root/.tipboard

EXPOSE 22 7272
