FROM python:3.12-alpine

RUN mkdir -p /usr/src/forkitech/app_service
WORKDIR /usr/src/forkitech/app_service

COPY . /usr/src/forkitech/app_service

RUN pip install --upgrade pip
RUN pip3 install --upgrade  poetry==2.0.1

RUN python3 -m poetry config virtualenvs.create false \
    && python3 -m poetry install --no-interaction --no-ansi \
    && echo yes | python3 -m poetry cache clear . --all