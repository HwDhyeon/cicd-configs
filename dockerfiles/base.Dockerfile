FROM python:3.6.8

USER root

WORKDIR /root

ENV HOME=/root
ENV TZ=Asia/Seoul

COPY CI/requirements.base requirements.base
COPY download-spark.sh download-spark.sh

RUN apt -y update && \
    apt -y upgrade
RUN xargs apt -y install < requirements.base

RUN ./download-spark.sh
