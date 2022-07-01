# `python-base` sets up all our shared environment variables
# FROM python:3.9.10-slim as python-base
FROM python:3.9.10-slim

# python enviroment setup
ENV PYTHONUNBUFFERED=1 \
    # prevents python creating .pyc files
    PYTHONDONTWRITEBYTECODE=1 \
    \
    # pip
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    \
    # poetry
    # https://python-poetry.org/docs/configuration/#using-environment-variables
    POETRY_VERSION=1.1.13 \
    # make poetry install to this location
    POETRY_HOME="/opt/poetry" \
    # do not ask any interactive question
    POETRY_NO_INTERACTION=1



RUN apt-get update \
    && apt-get install --no-install-recommends -y \
        # deps for installing poetry
        curl wget \
        # deps for building python deps
        build-essential \
        libpq-dev gcc git


RUN set -xe

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python3

WORKDIR /api

COPY . /api

ENV PATH="$POETRY_HOME/bin:$PATH"
RUN poetry install


EXPOSE 8000

CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

