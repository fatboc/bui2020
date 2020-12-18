FROM alpine:3.8

RUN apk add --no-cache py3-pip python3 python3-dev mariadb-dev build-base && \
    pip3 install flask requests Flask-Opentracing jaeger-client \
    flask-sqlalchemy mysqlclient flask-bootstrap flask-login flask-migrate \
    flask-wtf

COPY . /bui2020

ENV FLASK_APP app.py

WORKDIR /bui2020

CMD FLASK_CONFIG=production FLASK_APP=run.py flask run --host=0.0.0.0 --port=5000
