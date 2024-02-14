#!/bin/bash
rm -rf /usr/src/delta/migrations/versions/
mkdir -p /usr/src/delta/migrations/versions/
python3 /usr/src/delta/manage.py reset-db-version
python3 /usr/src/delta/manage.py db migrate
python3 /usr/src/delta/manage.py db upgrade
