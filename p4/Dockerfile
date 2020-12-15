FROM alpine:3.8

RUN apk add --no-cache py3-pip python3 python3-dev mariadb-dev build-base && \
    pip3 install flask requests Flask-Opentracing jaeger-client \
    flask-sqlalchemy mysqlclient

COPY . /app

ENV FLASK_APP app.py

WORKDIR /app

CMD flask run --host=0.0.0.0 --port=8000
