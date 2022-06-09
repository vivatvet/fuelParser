FROM python:3.9.9-alpine
COPY ./requirements.txt /
COPY ./src/* /app/
RUN apk add build-base && pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir --upgrade wheel && pip --no-cache-dir install -r /requirements.txt
WORKDIR /app/
