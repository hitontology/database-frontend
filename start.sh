#!/bin/sh
if [ ! -f "admin" ]
then
  flask fab create-admin --username admin --firstname admin --lastname admin --email nomail --password $HITO_DATABASE_PASSWORD
  touch admin
fi
flask run --host=0.0.0.0
