# Alpine doesn't work well with psycopg2
FROM python:slim

LABEL maintainer "Konrad Höffner (konrad.hoeffner@imise.uni-leipzig.de)"

WORKDIR /usr/src/app

COPY requirements.freeze.txt /tmp
RUN pip install -r /tmp/requirements.freeze.txt --disable-pip-version-check --no-cache-dir \
 && rm /tmp/requirements.freeze.txt
RUN secretKey=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 32 | head -n 1) \
 && echo "SECRET_KEY='$secretKey'" >> private.py

COPY app ./app
COPY config.py .
COPY start.sh .

EXPOSE 5000

ENV FLASK_APP=app
CMD ["/usr/src/app/start.sh"]

