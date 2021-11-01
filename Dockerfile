# Alpine doesn't work well with psycopg2
FROM python:slim

LABEL maintainer "Sebastian Stäubert (sebastian.staeubert@imise.uni-leipzig.de), Konrad Höffner (konrad.hoeffner@imise.uni-leipzig.de)"

WORKDIR /usr/src/app
#COPY app .
#COPY *.py .


COPY requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt --disable-pip-version-check --no-cache-dir \
 && rm /tmp/requirements.txt
RUN secretKey=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 32 | head -n 1) \
 && echo "SECRET_KEY='$secretKey'" >> private.py

EXPOSE 5000

ENV FLASK_APP=app
#CMD [ "flask", "fab", "create-admin" ]
CMD [ "flask", "run", "--host=0.0.0.0" ]

