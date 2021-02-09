FROM angora-dsl-base:latest

USER root

WORKDIR /root

COPY requirements.txt requirements.txt
COPY requirements-dev.txt requirements-dev.txt
COPY CI/requirements.ci requirements.ci
COPY CI/requirements-ci.txt requirements-ci.txt

RUN xargs apt install -y < requirements.ci

RUN pip install --upgrade pip && \
    pip install -r requirements.txt && \
    pip install -r requirements-dev.txt && \
    pip install -r requirements-ci.txt

RUN rm -rf requirements.txt && \
    rm -rf requirements-dev.txt
