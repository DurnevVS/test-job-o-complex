FROM python:3.12

COPY . /app
WORKDIR /app

RUN apt update -y
RUN pip install poetry
RUN poetry install --no-root