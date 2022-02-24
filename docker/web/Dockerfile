FROM python:3.10-alpine3.15

RUN apk add build-base

COPY requirements.txt /app/requirements.txt
WORKDIR /app

RUN pip install -r requirements.txt

CMD python app.py
