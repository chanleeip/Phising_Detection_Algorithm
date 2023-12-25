FROM python:3.12
WORKDIR /CLI
COPY . /CLI/
RUN pip3 install poetry
ARG ENV_FILE
COPY ${ENV_FILE:-.env} /CLI/.env
RUN poetry install --no-dev
RUN poetry update

