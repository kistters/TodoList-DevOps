FROM python:3.6.4-alpine3.7

ADD ./app /code

WORKDIR /code

RUN pip install -r requirements.txt