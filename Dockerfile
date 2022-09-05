FROM python:3.9-alpine3.14

RUN apk add build-base

COPY requirements.txt /app/requirements.txt
WORKDIR /app

RUN pip install -r requirements.txt

CMD python app.py
