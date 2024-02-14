#!/bin/bash

python3 /usr/src/delta/manage.py db migrate
python3 /usr/src/delta/manage.py db upgrade
