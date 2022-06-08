FROM python:3.10.5-alpine
COPY ./requirements.txt /
COPY ./src/* /app/
RUN apk add build-base && pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir --upgrade wheel && pip --no-cache-dir install -r /requirements.txt
ENV BOT_TOKEN=""
ENV DATABASE_PATH="/app/database.db"
WORKDIR /app/
ENTRYPOINT ["python", "/app/main.py"]
