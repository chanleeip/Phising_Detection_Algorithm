FROM python:3.12
ARG ENV_FILE

WORKDIR /CLI
COPY . /CLI/
RUN pip3 install poetry
COPY ${ENV_FILE:-.env} /CLI/.env


RUN poetry install --no-dev
CMD ["--path", "/default/path"]