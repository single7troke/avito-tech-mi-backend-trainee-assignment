FROM python:3.8

WORKDIR /statistic_parser

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update
RUN pip install --upgrade pip
RUN pip install sqlalchemy psycopg2 requests

COPY . /statistic_parser/

