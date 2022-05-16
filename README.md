## :warning: **The HITO Database Frontend is neither used nor maintained anymore**
This repository has been archived on 2022-05-16.

# HITO Database Frontend
[![License: MIT](https://img.shields.io/badge/license-MIT-blue)](LICENSE)

Create, read, update and delete (CRUD) tool for HITO software products and citations.

## Usage

The source of truth of HITO is the [ontology repository](https://github.com/hitontology/ontology), which is regularily mirrored in the [HITO SPARQL endpoint](https://hitontology.eu/sparql).
This frontend is the only Docker container in our setup that preserves state, so tell [@KonradHoeffner](https://github.com/konradhoeffner/) when you want to use it so he will not rebuild the docker containers and volumes during that time and performs a [semi-automatic merge into the ontology repository](https://github.com/hitontology/database/#export) afterwards.
**Otherwise, all your changes will be lost!**

## History
Generic RDF CRUD tools were not well suited to HITO software product data entry by domain experts without expert Semantic Web knowledge.
Thus, the relevant parts of HITO were transformed in 2020 into a [relational database](https://github.com/hitontology/database).
The assumption was that the relational database (in the following just "database") field would offer mature out-of-the-box generic CRUD tools.
However database experts told us that this is still an open problem so the next best step was the use of the simple and rapid CRUD application development framework [Flask-AppBuilder](https://flask-appbuilder.readthedocs.io/en/latest/).
If you know how to edit RDF Turtle files and don't need the features of the frontend, you can [edit the files directly](https://github.com/hitontology/ontology/), so that a merge is not necessary.
It is unclear whether the frontend will be used after the project end in July 2022.
Nowadays it is only developed and used as part of the [HITO Docker container infrastructure](https://github.com/hitontology/docker).
If you want to develop it without docker and the database is already running at myhost:myport, follow the old documentation below.

##  Setup

Run `. init.sh` or the following commands: 

    $ echo "PASSWORD = 'inserthitodatabasepasswordhere' > private.py"
    $ python -m venv venv
    $ . venv/bin/activate
    (venv) $ pip install -r requirements.txt
    (venv) $ deactivate
    $. venv/bin/activate
    (venv) $ export FLASK_APP=app
    (venv) $ export HITO_DATABASE_HOST=myhost       # defaults to localhost
    (venv) $ export HITO_DATABASE_PORT=myport       # defaults to 5432
    (venv) $ export HITO_DATABASE_PASSWORD=insertpasswordhere

    (venv) $ flask fab create-admin

## Run
    $ . venv/bin/activate
    (venv) $ flask run
