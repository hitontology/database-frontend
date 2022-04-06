#!/bin/bash
for t in 1 2 4 8 16 32 0
do
  flask fab create-admin --username admin --firstname admin --lastname admin --email nomail --password $HITO_DATABASE_PASSWORD
  if [ "$?" == "0" ]
  then
    flask run --host=0.0.0.0
    break
  else
    >&2 echo -n "Failed to create admin user on the database. "
	if [ "$t" == "0" ]
	then
      >&2 echo "Aborting."
	  exit 1
    else
	  >&2 echo "Retrying in ${t} seconds."
      sleep $t
	fi
  fi
done
